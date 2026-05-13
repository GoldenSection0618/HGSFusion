import torch
import importlib
from functools import partial
from torch.utils.data import DataLoader
from torch.utils.data import DistributedSampler as _DistributedSampler

from pcdet.utils import common_utils

from .dataset import DatasetTemplate
from .kitti.kitti_dataset import KittiDataset
from .custom.custom_dataset import CustomDataset
from pcdet.datasets.kitti.vod_dataset import VODDataset
from .kitti.tj4d_dataset import TJ4DDataset


def _make_missing_dataset_class(dataset_name, dependency_name, import_error):
    class _MissingDataset:
        def __init__(self, *args, **kwargs):
            raise ModuleNotFoundError(
                f'{dataset_name} requires optional dependency `{dependency_name}`. '
                f'Please install `{dependency_name}` to use this dataset.'
            ) from import_error

    _MissingDataset.__name__ = dataset_name
    return _MissingDataset


def _optional_dataset_import(module_name, dataset_name, dependency_name=None):
    try:
        module = importlib.import_module(module_name, package=__name__)
        return getattr(module, dataset_name)
    except ModuleNotFoundError as e:
        missing_dep = dependency_name or e.name or module_name
        return _make_missing_dataset_class(dataset_name, missing_dep, e)


NuScenesDataset = _optional_dataset_import('.nuscenes.nuscenes_dataset', 'NuScenesDataset')
WaymoDataset = _optional_dataset_import('.waymo.waymo_dataset', 'WaymoDataset')
PandasetDataset = _optional_dataset_import('.pandaset.pandaset_dataset', 'PandasetDataset')
LyftDataset = _optional_dataset_import('.lyft.lyft_dataset', 'LyftDataset')
ONCEDataset = _optional_dataset_import('.once.once_dataset', 'ONCEDataset')
Argo2Dataset = _optional_dataset_import('.argo2.argo2_dataset', 'Argo2Dataset', dependency_name='av2')

__all__ = {
    'DatasetTemplate': DatasetTemplate,
    'KittiDataset': KittiDataset,
    'NuScenesDataset': NuScenesDataset,
    'WaymoDataset': WaymoDataset,
    'PandasetDataset': PandasetDataset,
    'LyftDataset': LyftDataset,
    'ONCEDataset': ONCEDataset,
    'CustomDataset': CustomDataset,
    'VODDataset': VODDataset,
    'TJ4DDataset': TJ4DDataset,
    'Argo2Dataset': Argo2Dataset
}


class DistributedSampler(_DistributedSampler):

    def __init__(self, dataset, num_replicas=None, rank=None, shuffle=True):
        super().__init__(dataset, num_replicas=num_replicas, rank=rank)
        self.shuffle = shuffle

    def __iter__(self):
        if self.shuffle:
            g = torch.Generator()
            g.manual_seed(self.epoch)
            indices = torch.randperm(len(self.dataset), generator=g).tolist()
        else:
            indices = torch.arange(len(self.dataset)).tolist()

        indices += indices[:(self.total_size - len(indices))]
        assert len(indices) == self.total_size

        indices = indices[self.rank:self.total_size:self.num_replicas]
        assert len(indices) == self.num_samples

        return iter(indices)


def build_dataloader(dataset_cfg, class_names, batch_size, dist, root_path=None, workers=4, seed=None,
                     logger=None, training=True, merge_all_iters_to_one_epoch=False, total_epochs=0, tta=False):

    dataset = __all__[dataset_cfg.DATASET](
        dataset_cfg=dataset_cfg,
        class_names=class_names,
        root_path=root_path,
        training=training,
        logger=logger,
        tta=tta,
    )

    if merge_all_iters_to_one_epoch:
        assert hasattr(dataset, 'merge_all_iters_to_one_epoch')
        dataset.merge_all_iters_to_one_epoch(merge=True, epochs=total_epochs)

    if dist:
        if training:
            sampler = torch.utils.data.distributed.DistributedSampler(dataset)
        else:
            rank, world_size = common_utils.get_dist_info()
            sampler = DistributedSampler(dataset, world_size, rank, shuffle=False)
    else:
        sampler = None
    dataloader = DataLoader(
        dataset, batch_size=batch_size, pin_memory=True, num_workers=workers,
        shuffle=(sampler is None) and training, collate_fn=dataset.collate_batch,
        drop_last=False, sampler=sampler, timeout=0, worker_init_fn=partial(common_utils.worker_init_fn, seed=seed)
    )

    return dataset, dataloader, sampler

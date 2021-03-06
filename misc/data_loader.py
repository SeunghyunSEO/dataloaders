from torch.utils.data import DataLoader


class ValidationDataLoader(DataLoader):
    def __init__(self, dataset, **kwargs):
        kwargs['batch_size'] = 1
        super(ValidationDataLoader, self).__init__(dataset, **kwargs)

    def __iter__(self):
        iterator = super(ValidationDataLoader, self).__iter__()
        for batch in iterator:
            batch['sound'] = batch['sound'].view(batch['sound'].size()[1:])
            yield batch


if __name__ == "__main__":
    from misc.transforms import get_test_transform
    from librispeech.torch_readers.dataset_h5py import H5PyDataset

    test_transforms = get_test_transform(length=2 ** 14)
    test_dataset = H5PyDataset("./librispeach/train-clean-100.hdf5",
                               transforms=test_transforms,
                               sr=16000,
                               one_hot_utterance=True,
                               in_memory=False)
    params = {'batch_size': 64,
              'shuffle': True,
              'num_workers': 1}
    test_generator = ValidationDataLoader(test_dataset, **params)
    for batch in test_generator:
        print(batch['sound'].shape)
        print(batch)
        break

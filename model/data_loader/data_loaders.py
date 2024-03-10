from torchvision import datasets, transforms
from base import BaseDataLoader, StockDataset


class StockDataLoader(BaseDataLoader):
    """
    MNIST data loading demo using BaseDataLoader
    """
    def __init__(self, window_size, target_day, transform_type, pickle_dir, csv_dir, batch_size, shuffle=True, validation_split=0.0, num_workers=1, training=True):
        self.dataset = StockDataset(window_size, target_day, transform_type, pickle_dir, csv_dir)
        
        super().__init__(self.dataset, batch_size, shuffle, validation_split, num_workers)
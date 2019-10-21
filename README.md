# Data-Augmentation

The data augmentation process comprises of three step. First, define all the transformations permissable with associated probabiities and options with their associated probabilities if desired. The augment_settings function produces a dictionary output that defines the augmentation policy fully in a standard way and accept a number of possible input formats. This dictionary serves as an input to the choose_augment which samples from the distribution defined by the augmentation policy in order to apply it to images or batches of images. Once selected, this is applied by the apply_augment function.

__augment_settings__: 

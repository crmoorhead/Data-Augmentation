# Data-Augmentation

The data augmentation process comprises of three step. First, define all the transformations permissable with associated probabiities and options with their associated probabilities if desired. The augment_settings function produces a dictionary output that defines the augmentation policy fully in a standard way and accept a number of possible input formats. This dictionary serves as an input to the choose_augment which samples from the distribution defined by the augmentation policy in order to apply it to images or batches of images. Once selected, this is applied by the apply_augment function.

__augment_settings(policy_dict,\*args,\*\*kwargs)__: The purpose of this function is to produce a standardised input for the choose_augment function that will give instructions about how we pick which policies are applied to each image. The output of this function has a standard dictionary form which will contains entries with keywords corresponding to names of transformations and values consisting of a standard dictionary form whose definition follows. In addiition to one entry for each transformation, there is one additional dictionary entry with key "policy_probs" which gives the probabilities of each transformation (including no transformations) being chosen. This can be explicitly set using the optional "probs" keyword whose value is a list of probabilities corresponding to the order the transformations are given in the policy_dict. This may or may not include  the "None" transformation. By default, the "None" transforamtion is added into the viable options and the "policy_probs" will be evaluated as giving equal probability to all transformation, including the "None" transformation. 

The standard dictionary form for each transformation consists of three keywords "main_args", "opt_args" and "opt_kwargs" which have values corresponding to the main arguments (that is, the compulsory inputs), the optional arguments and the optional keyword arguments of that transformation. The details of each are given in dictionary form. "main_args" has two entries, "options" and "probs" which give the options for each of the compulsory arguments in the form of a list of lists and a one to one corresponding list of lists for the probability of each option. "opt_args" has the same two entries, with values being set to be a list of strings or lists of strigns. Note that optional arguments are not mutually exclusive. Say that "extra_1" and "extra_2" are two possible optional functionalities of a given transformation, then one, both or neither can be applied and the probabilities associated are independent. In some cases, optional arguments _are_ mutually exclusive - images cannot be both "color" and "greyscale". We combine these examples as:

          "opt_args": {"options":["extra_1","extra_2,["color","grayscale"]],"probs":[0.5,0.5,[0.5,[0.5,0.5]]

The "probs" entry gives the independent probability of each optional argument occurring or, in the case of mutually exclusive arguments, the joint probability of any of the mutually exclusive options occurring followed by a list detailing the probability of each option. This functionality does not cover all possible structures, but it is sufficiently flexible and can be borne in mind when designing new transformations. For the "opt_kwargs" there are four items defined: "options","k_probs","values" and "v_probs". The first two take the same form as the "opt_args" in that keyword arguments can be used in conjunction with one another and are not mutually exclusive with the first defining recognised keywords and the second the associated probabilities. The last two are the same form as the entries for "options" and "probs" in "main_args" in that each chosen keyword must have one, and only one, value it takes on. "values" and "v_probs" define the possible values and probabilities. 
          
While the output of this function is standard, the input is non-standard and can be designed in a such a way as to describe the augmentation policy in as simple a way as possible. To define all of these explicitly would be extremely tedious and should only be necessary for the finest degree of control. Instead we have the following permissible inputs.

          transformation_example=[1,2,3]
          
This defines a function with only one compulsory argument that can take on the value 1, 2 or 3 with equal probability.

          transformation=(0,1)
          
Defines a function with one compulsory argment which is a random variable taken from the interval (0,1) using a uniform distribution.

          transformation_example=[[1,2,3],(3,4)]
          
This defines a function that has two compulsory arguments. The first can take on the value 1, 2 or 3 with equal probability and the second is chosen from a uniform distribustion over (3,4).





          transformation={"main":[],p

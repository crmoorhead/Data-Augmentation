# Data-Augmentation

The data augmentation process comprises of three step. First, define all the transformations permissable with associated probabiities and options with their associated probabilities if desired. The augment_settings function produces a dictionary output that defines the augmentation policy fully in a standard way and accept a number of possible input formats. This dictionary serves as an input to the choose_augment which samples from the distribution defined by the augmentation policy in order to apply it to images or batches of images. Once selected, this is applied by the apply_augment function.

## Creating Augmentation Policies

The augment_settings function allows a high degree of functionality to specify which augmentations we want to apply, what the settings  and possible parameter values are for those augmentatons and with what probabity these can occur. The following gives a detailed explanation of the function as well as key examples. 

__augment_settings(policy_dict,\*args,\*\*kwargs)__: The purpose of this function is to produce a standardised input for the choose_augment function that will give instructions about how we pick which policies are applied to each image. 

The output of this function has a standard dictionary form which will contains entries detailing necessary aspects of the augmentation policy. It consists of five dictionary entries which contain lists or dictionaries themselves. They are:

 - _policies_: A list of strings of all transformations it is possible to apply. This always includes the "None" transformation where no policy is applied. 
 - _policy_probs_: The probability of the named transformations being selected. This is a list of floats in the range \[0,1\] that sums to 1. 
 - _main_: The options for each transformation for their compulsory arguments. This is a dictionary with a key for each transformation with values corresponding to a dictionary containing "options" and "probs". "options" is a list of lists with each sublist consisting of the options for the corresponding functional argument. "probs" is a one-to-one corresponding list of lists giving the probability of each option for each argument.
 - _opt\_args_: The options for each transformation for optional string arguments. Also a dictionary with a key for each transforamtion and values corresponding to a dictionary containing "options" and "probs". In contrast to _main_, the number of optional arguments is not a fixed number when it comes to choosing and implementing an augmentation. Except where they directly contradict, the probability that any two or more optional arguments are chosen is independent. The "options" entry contains a list of all optional arguments and is a list of strings and lists of strings beginning with the "None" option. Each independent option is represented by a string argument whereas collections of mutually exclusive keywords are represented by a list of strings. The "probs" argument details the probabilities of these argument
 - _opt\_kwargs_: The options for each transformation when it comes to optional keyword arguments and the values assignable to those keyword arguments. This is also a dictionary with a key for each transforamtion, but with values corresponding to a dictionary containing "options","k_probs","values" and "v_probs". The first two follow the form of the _opt\_args_ dictionary entries as the number of optional keyword arguments is also not fixed. The last two follow the from of the _main_ dictionary as each activated keyword must have one clearly defined value. 
 
Examples of this output for given inputs are given later.

For the input, we define a dictionary consisting of an entry for each transformation possible with one extra optional entry "probs" that we can assign explcit probabilities to the the transformations. If the "None" transformation is not specified, then it will be implemented in the output of the function, so if one wants the input to always be different from the output, then it should be specified and assigned a probability of zero in thr "probs" keyword argument. If no probabilities are specified for the transformations, they will be automatically assigned an equal probability of occurring 

This can be explicitly set using the optional "probs" keyword whose value is a list of probabilities corresponding to the order the transformations are given in the policy_dict. This may or may not include  the "None" transformation. By default, the "None" transforamtion is added into the viable options and the "policy_probs" will be evaluated as giving equal probability to all transformation, including the "None" transformation. 

The following is an example of a fully defined augmentation policy for five transformations:

    test_standard=augment_settings({"None":\[\],
                                    "transform_1":{"main":\[\[1,2,3,4\],(-1,1)\],"opt_args":\["poss_1","poss_2"\],
                                                "opt_kwargs":{"options":\["test",\["left","right","centre"\]\], 
                                                              "values":    {"test":\[0,1\],"left":\[50\],"right":\[-50\],"centre":\["what","no"\]}}},
                                   "transform_2":{"main":{"options":[(0,1),[1,2,3,4]],"probs":["normal",[0.1,0.2,0.3,0.4]]},
                                                 "opt_args":["None",["Yes","No"],"Buggerit"]},
                                   "transform_3":{"main":{"options":[(0,1),[1,2,3,4]]},
                                                  "opt_kwargs":{"just":[5,10,15,20],"THis":0, "Test":["yes","no"]}},
                                   "transform_4":[1,2,3,4],
                                   "transform_5":(0,1),
                                   "transform_6":[[1,2,3,4],(0,1)]},
                                   probs=[0]+[1/6]*6)

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

          transformation_example={"main":{"options":[[1,2],(0,1)],"probs":[[0.2,0.8],"normal"]}}
          
In the above, we specify all probabilities explicitly. The first compulsory argument chooses the value 1 with probability 0.2 and 2 with probability 0.8. The second compulsory argument chooses a value taken from a normal distribution derived from the interval (0,1). This normal distibution will have mean of the centre of the interval (in this case 0.5) and standard deviation of one quarter of the interval (95% of values chosen by this will be within the stated interval). Currently, the only options for values chosen from an interval are "uniform" and "normal" but more will be added in future. For the majority of functions, equal probability is likely to be enough but extra functionality is useful.

If we have optional arguments and keyword arguments for a function, we must define the dictionary format as per the last example and add extra keywords for "opt_args" and "opt_kwargs" as described previously. The only not to make is that the probabilities for each argument, keyword argument and keyword value do not need to be defined explicitly unless desired. An automatic assignment is implemented similar to that of the compulsory arguments in the first example. Take the following example:

          transformation_example={"main":{"options":[[1,2],(0,1)],"probs":[[0.2,0.8],"normal"]}
                                  "opt_args":["extra_1","extra_2",["extra_3A","extra_3B"],
                                  "opt_kwargs":{"options":["foo","bar"],"values":[[0,1,2],(0,1)]}}

There are no probabilties for the "opt_args" and "opt_kwargs" specified, only the valid arguments, keywords and values for each keyword. For "opt_args", the "probs" entry in the dictionary assigns a probability of 0.5 to no argument being used. If "None" is not chosen, then each of the possible arguments appliable are activated with probability 0.5. Where two or more options are mutually exclusive, they are assigned a joint probability of 0.5 and then one of the options is chosen with equal probability. For "opt_kwargs", the keyword choice follows the same pattern as "opt_args" and the values of each keyword follow the patten of "main". The above generates a augmentation policy subobject that is given by:
 
                    transformation_example={"main":{"options":[[1,2],(0,1)],"probs":[[0.2,0.8],"normal"]}
                                  "opt_args":{"options":["None","extra_1","extra_2",["extra_3A","extra_3B"],
                                              "probs":[0.5,0.5,0.5,[0.5,[0.5.0.5]]]}
                                  "opt_kwargs":{"options":["None","foo","bar"],"k_probs":[0.5,0.5,0.5]
                                                "values":[[0,1,2],(0,1)], "v_probs":[[1/3,1/3,1/3],"uniform"]}}
 
As mentioned at the beginning of this section, the goal is to produce an object of this format for each transformation in an augmentation policy and the output of the augmentation_settings function is a dictionary of such objects. 

## Choosing and Applying a Transformation (or Transformations)

With the transformation settings object defined, we can use it as a standard input 


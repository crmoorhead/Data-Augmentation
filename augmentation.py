# Code for implementing data augmentation

import numpy as np
from numpy.random import choice, normal, uniform

def augment_settings(policy_dict,*args,**kwargs):
    policies=[p for p in policy_dict]
    if "None" not in policies and None not in policies:                            # Add no transformations
        policies.append("None")
    if "probs" in kwargs:            # Note that no transformation must be stated with a probability if it is to be an option.
        policy_probs=kwargs["probs"]
    else:
        policy_probs=[1/len(policy_dict)]*len(policy_dict) # If no probs stated, all transformations assigned equal chance


    # For each policy, we take in the compulsory arguments and determine their type, followed by the optional arguments. These
    # arguments can have the form of a list of options or a choice taken from an interval. Again, each of these may have an
    # associated probability distribution

    main_args={}
    opt_args={}
    opt_kwargs={}

    # for each policy - a tuple means an interval choice for a single mandatory input
    #                 - a list of tuples

    # Note that mutually exclusive options appear in a list together

    for p in policy_dict:
        if p=="None":
            pass
        elif policy_dict[p] in [{},[],None,"None"]:
            main_args[p]={}
            opt_args[p]={}
            opt_kwargs[p]={}
        else:
            if  policy_dict[p].__class__==dict:   # check if the policy options are a dictionary. This means that either
                if "main" in policy_dict[p]:    # It has a dictionary for main options [1]
                    main_args[p]={}
                    if policy_dict[p]["main"].__class__==list:  # with only options in list format [2]
                        main_args[p]["options"]=policy_dict[p]["main"] # We create the correct dict entry for output
                        main_args[p]["probs"]=[] # Create an empty dict entry for associated probabilities
                        for m in main_args[p]["options"]: # For every compulsory option
                            if m.__class__==list:
                                main_args[p]["probs"].append([1/len(m)]*len(m))  # for a list, each option is given equal liklihood
                            elif m.__class__==tuple: # for an interval, we select from a uniform distribution
                                main_args[p]["probs"].append("uniform")
                            else:
                                print("Type error in main options of",p) # Only list or interval are valid options
                    elif policy_dict[p]["main"].__class__==dict and "options" in policy_dict[p]["main"]: # Or it is a dict [2]
                        if "probs" in policy_dict[p]["main"]:
                            main_args[p]={"options":policy_dict[p]["main"]["options"],"probs":policy_dict[p]["main"]["probs"]}
                        else:
                            main_args[p]={"options":policy_dict[p]["main"]["options"]} # Write the options to standard dictionary
                            main_args[p]["probs"]=[] # Create an empty dict entry for associated probabilities
                            for m in main_args[p]["options"]: # For every compulsory option
                                if m.__class__==list:
                                    main_args[p]["probs"].append([1/len(m)]*len(m))  # for a list, each option is given equal liklihood
                                elif m.__class__==tuple: # for an interval, we select from a uniform distribution
                                    main_args[p]["probs"].append("uniform")
                                else:
                                    print("Type error in main options of",p) # Only list or interval are valid options
                else:
                    main_args[p]={}

                # If we do have some optional arguments, they will be a text descriptor and the input here will either be strings or
                # lists of strings where the members of the list are mutually exclusive. eg.we cannot have both "greyscale" and "color"

                # All augmentations mut have a "None" argument option that occurs with a given probability
                # The rest of the time, independent args are activated with a given probability for each
                # If they are mutually exclusive, that option is activated with given probability an a choice is made by random
                # If all conditional rolls fail, then we reselect.

                # [0.5, [0.5,0.5,0.5,[0.5,0.3,0.7]]]

                if "opt_args" in policy_dict[p]:
                    opt_args[p]={}
                    if policy_dict[p]["opt_args"].__class__==list: # If the policy is a list
                        opt_args[p]["options"]=policy_dict[p]["opt_args"]
                        if "None" not in opt_args[p]["options"]:
                            opt_args[p]["options"].insert(0,"None")
                        opt_args[p]["probs"]=[1/(len(opt_args[p]["options"]))]  # With prob 1/(number of options), nada
                        if np.all([i.__class__==str for i in policy_dict[p]["opt_args"]])==True: # If a list is all strings, do
                            for i in range(len(policy_dict[p]["opt_args"])-1):
                                opt_args[p]["probs"].append(0.5) # Each occurs with prob 0.5
                        else:
                            for o in policy_dict[p]["opt_args"]:
                                if o.__class__==str:
                                    if o!="None":
                                        opt_args[p]["probs"].append(0.5)
                                elif o.__class__==list:
                                    current=[0.5]
                                    for sub in o:
                                        if sub.__class__==str:
                                            current.append(1/len(o))
                                        else:
                                            print("Not a valid set of optional arguments")
                                    opt_args[p]["probs"].append(current)
                                else:
                                    print("Not a valid set of optional arguments")

                    elif policy_dict[p]["opt_args"].__class__==dict and "options" in policy_dict[p]["opt_args"]:
                        if "probs" in policy_dict[p]["opt_args"]:
                            opt_args[p]={"options":policy_dict[p]["opt_args"]["options"],"probs":policy_dict[p]["opt_args"]["probs"]}
                    else:
                        print("Type error in optional args of",p)
                else:
                    opt_args[p]={}

                # opt_kwargs works in the same waye except that we must have values associated with the kwargs which are given probabilities

                if "opt_kwargs" in policy_dict[p]:
                    opt_kwargs[p]={}
                    if policy_dict[p]["opt_kwargs"].__class__==dict: # If the policy is a dictionary
                        if "options" in policy_dict[p]["opt_kwargs"]:  # If there is an options kword
                            if "values" in policy_dict[p]["opt_kwargs"]:
                                opt_kwargs[p]["options"]=policy_dict[p]["opt_kwargs"]["options"]
                                opt_kwargs[p]["values"]=policy_dict[p]["opt_kwargs"]["values"] # then there will be the correct content
                                if "k_probs" in policy_dict[p]["opt_kwargs"]:
                                    opt_kwargs[p]["k_probs"]=policy_dict[p]["opt_kwargs"]["k_probs"]
                                else:
                                    opt_kwargs[p]["k_probs"]=[]
                                    if "None" not in opt_kwargs[p]["options"]: # If just a list of options, all given prob 0.5 of happening
                                        opt_kwargs[p]["options"].insert(0,"None")
                                        opt_kwargs[p]["k_probs"].append(1/len(opt_kwargs[p]["options"]))
                                    elif opt_kwargs[p]["options"]["None"].__class__==float or opt_kwargs[p]["options"]["None"].__class__==int: # If prob of
                                        opt_kwargs[p]["k_probs"].append(opt_kwargs[p]["options"]["None"]) # If int or float, add
                                    for o in opt_kwargs[p]["options"]:
                                        if o.__class__!=list and o!="None":
                                            opt_kwargs[p]["k_probs"].append(0.5)
                                        elif o!="None":
                                            opt_kwargs[p]["k_probs"].append([0.5]+[1/len(o)]*len(o))
                                        else:
                                            pass

                                if "v_probs" in policy_dict[p]["opt_kwargs"]:
                                    opt_kwargs[p]["v_probs"]=policy_dict[p]["opt_kwargs"]["v_probs"]
                                else:
                                    opt_kwargs[p]["v_probs"]={}
                                    for kv in opt_kwargs[p]["values"]:
                                        opt_kwargs[p]["v_probs"][kv]=[]
                                        for v in opt_kwargs[p]["values"][kv]:
                                            if v.__class__!=list:
                                                opt_kwargs[p]["v_probs"][kv].append(1/len(opt_kwargs[p]["values"][kv]))
                                            else:
                                                opt_kwargs[p]["v_probs"][kv].append([1/len(opt_kwargs[p]["values"][kv])]+[1/len(v)]*len(v))

                            else:
                                print("ERROR: No associated values with keywords")
                        else:
                            opt_kwargs[p]["options"]=[]
                            opt_kwargs[p]["k_probs"]=[]
                            opt_kwargs[p]["values"]={}
                            opt_kwargs[p]["v_probs"]={}
                            for k in policy_dict[p]["opt_kwargs"]:
                                 opt_kwargs[p]["options"].append(k)
                            if "None" not in opt_kwargs[p]["options"]: # If just a list of options, all given prob 0.5 of happening
                                opt_kwargs[p]["options"].insert(0,"None")
                                opt_kwargs[p]["k_probs"].append(1/len(opt_kwargs[p]["options"]))
                                opt_kwargs[p]["k_probs"]+=[0.5]*(len(opt_kwargs[p]["options"])-1)
                            elif opt_kwargs[p]["options"]["None"].__class__==float or opt_kwargs[p]["options"]["None"].__class__==int: # If prob of
                                opt_kwargs[p]["k_probs"].append(opt_kwargs[p]["options"]["None"])
                                opt_kwargs[p]["k_probs"]+=[1/len(opt_kwargs[p]["options"])]*len(opt_kwargs[p]["options"])
                            for k in policy_dict[p]["opt_kwargs"]:
                                if policy_dict[p]["opt_kwargs"][k].__class__ != list:
                                    opt_kwargs[p]["values"][k]=[policy_dict[p]["opt_kwargs"][k]]
                                else:
                                    opt_kwargs[p]["values"][k]=policy_dict[p]["opt_kwargs"][k]
                            for kv in opt_kwargs[p]["values"]:
                                opt_kwargs[p]["v_probs"][kv]=[]
                                for v in opt_kwargs[p]["values"][kv]:
                                    if v.__class__!=list:
                                        opt_kwargs[p]["v_probs"][kv].append(1/len(opt_kwargs[p]["values"][kv]))
                                    else:
                                        opt_kwargs[p]["v_probs"][kv].append([1/len(opt_kwargs[p]["values"][kv])]+[1/len(v)]*len(v))


                    else:
                        print("Type error in optional args of",p)
                else:
                    opt_kwargs[p]={}


            # Check all in list

            elif policy_dict[p].__class__==list: # OR it is a list [1]
                if policy_dict[p][0].__class__!=list:
                    main_args[p]={}
                    main_args[p]["options"]=[policy_dict[p]]
                    main_args[p]["probs"]=[[1/len(policy_dict[p])]*len(policy_dict[p])]
                else:  # Otherwise we assume that it is a list of lists, each of which represents options of a compulsory argument
                    main_args[p]={"options":[],"probs":[]}
                    for pl in policy_dict[p]:
                        main_args[p]["options"].append(pl)
                        if pl.__class__==list:
                            main_args[p]["probs"].append([1/len(pl)]*len(pl))
                        elif pl.__class__==tuple:
                            main_args[p]["probs"].append("uniform")
                opt_args[p]={}
                opt_kwargs[p]={}


            elif policy_dict[p].__class__==tuple and len(policy_dict[p])==2: # OR if it is a single tuple [1]
                main_args[p]={}
                main_args[p]["options"]=[policy_dict[p]]
                main_args[p]["probs"]=["uniform"]
                # opt_args and opt_kwargs are empty dictionaries
                opt_args[p]={}
                opt_kwargs[p]={}
            else:
                print("Inputs for ",p,"not defined properly")

    standard_policy_dict={"policies":policies,"policy_probs":policy_probs, "main":main_args,
                          "opt_args":opt_args,"opt_kwargs":opt_kwargs}

    return standard_policy_dict

def choose_augment(settings_dict,*args,**kwargs):

    # pick first transformation
    transform_1=choice(settings_dict["policies"],p=settings_dict["policy_probs"])
    if transform_1 in ["None",None]:
        if "print_policies" in args:
            print("None applied")
        return ["None",[],[],[],[]]
    # pick compulsory arguments
    comp_args=[]
    if "options" in settings_dict["main"][transform_1]:
        for m in range(len(settings_dict["main"][transform_1]["options"])):
            if settings_dict["main"][transform_1]["options"][m].__class__==list:
                main_choice=choice(settings_dict["main"][transform_1]["options"][m],
                                   p=settings_dict["main"][transform_1]["probs"][m])
            else:
                if settings_dict["main"][transform_1]["probs"][m]=="uniform":
                    main_choice=uniform(settings_dict["main"][transform_1]["options"][m][0],
                                        settings_dict["main"][transform_1]["options"][m][1])
                elif settings_dict["main"][transform_1]["probs"][m]=="normal":
                    mean=((settings_dict["main"][transform_1]["options"][m][1]-settings_dict["main"][transform_1]["options"][m][0])/2)
                    sd=(mean-settings_dict["main"][transform_1]["options"][m][0])/2
                    main_choice=normal(mean,sd)
                else:
                    print("not a valid probability distribution")
                    print(settings_dict["main"][transform_1]["probs"][m])
                    return(None)
            comp_args.append(main_choice)

    # pick optional args
    opt_args=[]
    if settings_dict["opt_args"][transform_1]!={}:
        if uniform()<settings_dict["opt_args"][transform_1]["probs"][0]: # With given prob, no optional args added
            pass
        else:
            while opt_args==[]:   # While we have not chosen any arguments
                for a in range(1,len(settings_dict["opt_args"][transform_1]["options"])): # For all arguments that are not None
                    if settings_dict["opt_args"][transform_1]["options"][a].__class__==list: # If a list
                        if uniform()<settings_dict["opt_args"][transform_1]["probs"][a][0]: # One of them is chosen
                            arg_choice=choice(settings_dict["opt_args"][transform_1]["options"][a],
                                              p=settings_dict["opt_args"][transform_1]["probs"][a][1:])
                            opt_args.append(arg_choice)
                    else:
                        if uniform()<settings_dict["opt_args"][transform_1]["probs"][a]:
                            arg_choice=settings_dict["opt_args"][transform_1]["options"][a]
                            opt_args.append(arg_choice)
    # pick optional kwargs
    opt_kwargs=[]
    if settings_dict["opt_kwargs"][transform_1]!={}:
        if uniform()<settings_dict["opt_kwargs"][transform_1]["k_probs"][0]: # With given prob, no optional args added
            pass
        else:
            while opt_kwargs==[]:   # While we have not chosen any arguments
                for a in range(1,len(settings_dict["opt_kwargs"][transform_1]["options"])): # For all arguments that are not None
                    if settings_dict["opt_kwargs"][transform_1]["options"][a].__class__==list: # If a list
                        if uniform()<settings_dict["opt_kwargs"][transform_1]["k_probs"][a][0]: # One of them is chosen
                            kwarg_choice=choice(settings_dict["opt_kwargs"][transform_1]["options"][a],
                                              p=settings_dict["opt_kwargs"][transform_1]["k_probs"][a][1:])
                            opt_kwargs.append(kwarg_choice)
                    else:
                        if uniform()<settings_dict["opt_kwargs"][transform_1]["k_probs"][a]:
                            kwarg_choice=settings_dict["opt_kwargs"][transform_1]["options"][a]
                            opt_kwargs.append(kwarg_choice)
    # pick values for optional kwargs
    opt_kvals=[]
    if opt_kwargs!=[]:
        for kw in opt_kwargs:
            kval_choice=choice(settings_dict["opt_kwargs"][transform_1]["values"][kw],
                               p=settings_dict["opt_kwargs"][transform_1]["v_probs"][kw])
            opt_kvals.append(kval_choice)

    # Option to print
    if "print_policies" in args:
        print(transform_1)
        print("Mandatory args",comp_args)
        print("Optional args:",opt_args)
        print("Optional kwargs:",opt_kwargs)
        print("Values for optional kwargs:",opt_kvals)

    return [transform_1,comp_args,opt_args,opt_kwargs,opt_kvals]

def apply_augment(im,policy_dict,functional_dict,*args,**kwargs):
    transformations=[choose_augment(policy_dict,*args,**kwargs)]
    print(transformations[0][0])
    if "serial_transformations" in kwargs and transformations[0][0]!="None":
        current=0
        while random()<kwargs["serial_transformations"][current] and current+1<len(kwargs["serial_transformations"]):
            print("Pick another")
            new_transformation=choose_augment(policy_dict,*args,**kwargs)
            while new_transformation[0] in ["None"]+[t[0] for t in transformations]:
                new_transformation=choose_augment(policy_dict,*args,**kwargs)
            transformations.append(new_transformation)
            print(transformations[current+1][0])
            current+=1
    for t in transformations:
        print(t[1],t[2],{t[3][i]:t[4][i] for i in range(len(t[3]))})
        if t[0]!="None":
            if len(t[1])==0:
                im=functional_dict[t[0]](im,*list(args)+t[2],**{**kwargs,**{t[3][i]:t[4][i] for i in range(len(t[3]))}})
            elif len(t[1])==1:
                im=functional_dict[t[0]](im,t[1][0],*list(args)+t[2],**{**kwargs,**{t[3][i]:t[4][i] for i in range(len(t[3]))}})
            elif len(t[1])==2:
                im=functional_dict[t[0]](im,t[1][0],t[1][1],*list(args)+t[2],**{**kwargs,**{t[3][i]:t[4][i] for i in range(len(t[3]))}})
            elif len(t[1])==3:
                im=functional_dict[t[0]](im,t[1][0],t[1][1],t[1][2],*list(args)+t[2],**{**kwargs,**{t[3][i]:t[4][i] for i in range(len(t[3]))}})
            else:
                print("Currently not supporting more than 3 mandatory arguments")
    return im

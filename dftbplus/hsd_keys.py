
'''
DFTB+ input keywords and type
Keywords are restricted to CamelCase as written in official manual
'''
type_key = { 
             'float' : { 
                         'SCCTolerance',
                         'Temperature',
                         'MixingParameter',
                         'MaxForceComponent',    # in Driver:[different methods]
                         'MaxAtomStep',     # in Driver:[different methods]
                        },
             'int': {
                         'ParserVersion',
                         'MaxSCCIterations',
                         'CachedIterations',
                         'MaxSteps',    # in Driver:[different methods]
                        },
             'str': { 
                         'Prefix', 
                         'Separator', 
                         'Suffix', 
                         'MovedAtoms',    # in Driver:[different methods]
                         'Atoms',   # in Analysis:ProjectStates
                         'Label',   # in Analysis:ProjectStates
                        },
             'bool': {
                         'SCC',
                         'ShellResolved',   # in Analysis:ProjectStates
                         'OrbitalResolved',   # in Analysis:ProjectStates
                        },
            }

# build inverse relation
key_type = {value: key for key, values in type_key.items() for value in values}

special_blocks = [ # keywords with content not suitable for recursive dictionary parsing  
        'Geometry', # Gen form or read isolated file
        'MaxAngularMomentum', # Keys are atomic symbols, value could be complicated
        'ProjectStates',  # Repeated 'Region' key
        'KPointsAndWeights', # lines of arrays
        ]


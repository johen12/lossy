import pandas as pd
import numpy as np

# Levy Russian data
levy_exp1a_verb = pd.DataFrame({
    "Mean reading time (ms)": 600 + 800/276 * np.array([28, 211, 36, 154]),
    "Relative clause type": ["SRC", "SRC", "ORC", "ORC"],
    "Locality": ["local", "non-local", "local", "non-local"]
})

levy_exp1b_verb = pd.DataFrame({
    "Mean reading time (ms)": 400 + 1200/955 * np.array([178, 549, 188, 861]),
    "Relative clause type": ["SRC", "SRC", "ORC", "ORC"],
    "Locality": ["local", "non-local", "local", "non-local"]
})

levy_exp2a_verb = pd.DataFrame({
    "Mean reading time (ms)": np.concatenate((
        600 + 500/260  * np.array([-10 + 12, 23 + 53, 40 + 59, -10 + 12]),
        600 + 1000/351 * np.array([23 + 33, 37 + 56]))),
    "Number of interveners": [0, 1, 2, 0, 1, 2],
    "Intervener type": ["Argument", "Argument", "Argument", "Adjunct", "Adjunct", "Adjunct"],
})

husain_exp1_verb = pd.DataFrame({
    "Mean reading time (log ms)": 6.5 + 0.4/480 * np.array([371, 122, 142, 89]),
    "Relative clause type": ["SRC", "SRC", "ORC", "ORC"],
    "Locality": ["local", "non-local", "local", "non-local"]
})

husain_exp2_verb = pd.DataFrame({
    "Mean reading time (log ms)": 6.5 + 0.2/431 * np.array([155, 297, 0, 355]),
    "Predictability": ["high", "low", "high", "low"],
    "Distance": ["short", "short", "long", "long"]
})

safavi_exp1_verb = pd.DataFrame({
    "Mean reading time (ms)": 500 + 200/846 * np.array([151, 321, 330, 618]),
    "Predictability": ["high", "low", "high", "low"],
    "Distance": ["short", "short", "long", "long"]
})
import numpy as np

def gen_russian_grammar_exp2(
    p_src: np.float64, 
    p_src_local: np.float64,
    p_src_case_marked: np.float64,
    p_orc_local: np.float64,
    p_orc_case_marked: np.float64,
    p_one_arg: np.float64,
    p_adj_interveners: np.float64,
    p_one_adj: np.float64
) -> str:
    return f"""
    RC -> SRC [{p_src}] | ORC [{1-p_src}]
    SRC -> SRCRP 'V' ArgSRC [{p_src_local*(1-p_adj_interveners)}] | SRCRP ArgSRC 'V'  [{(1-p_src_local)*(1-p_adj_interveners)}] | SRCRP AdjIntv 'V' ArgSRC [{p_adj_interveners*p_src_local}] | SRCRP AdjIntv ArgSRC 'V' [{p_adj_interveners*(1-p_src_local)}]
    ArgSRC -> 'DO' [{p_one_arg}] | 'DO' 'IO' [{1-p_one_arg}]
    SRCRP -> 'RPNom' [{p_src_case_marked}] | 'chto' [{(1-p_src_case_marked)}]
    ORC -> ORCRP 'V' ArgORC [{p_orc_local*(1-p_adj_interveners)}] | ORCRP ArgORC 'V'  [{(1-p_orc_local)*(1-p_adj_interveners)}] | ORCRP AdjIntv 'V' ArgORC [{p_adj_interveners*p_orc_local}] | ORCRP AdjIntv ArgORC 'V' [{p_adj_interveners*(1-p_orc_local)}]
    ArgORC -> 'Subj' [{p_one_arg}] | 'Subj' 'IO' [{1-p_one_arg}]
    ORCRP -> 'RPAcc' [{p_orc_case_marked}] | 'chto' [{(1-p_orc_case_marked)}]
    AdjIntv -> 'Adj1' [{p_one_adj*0.5}] | 'Adj1' 'Adj2' [{(1-p_one_adj)*0.5}] | 'Adj2' [{p_one_adj*0.5}] | 'Adj2' 'Adj1' [{(1-p_one_adj)*0.5}]
    """

def gen_hindi_grammar_exp1(
    p_src: np.float64, 
    p_src_local: np.float64,
    p_obj_elision: np.float64,
    p_orc_local: np.float64,
    p_subj_elision: np.float64,
) -> str:
    return f"""
    RC -> SRC [{p_src}] | ORC [{1-p_src}]
    SRC -> 'RPErg' InnerSRC [{1-p_obj_elision}] | 'RPErg' 'V' [{p_obj_elision}]
    InnerSRC -> 'DO' 'V' [{1-p_src_local}] | 'V' 'DO' [{p_src_local}]
    ORC -> 'RPAcc' InnerORC [{1-p_subj_elision}] | 'RPAcc' 'V' [{p_subj_elision}]
    InnerORC -> 'Subj' 'V' [{1-p_orc_local}] | 'V' 'Subj' [{p_orc_local}]
    """

def gen_hindi_grammar_exp2(
    p_cp: np.float64,
    p_cp_intv: np.float64,
    p_cp_short: np.float64,
    p_cp_lightverb: np.float64,
    p_sp_intv: np.float64,
    p_sp_short: np.float64,
    p_sp_lightverb: np.float64,
) -> str:
    # return f"""
    # S -> CPP [{p_cp}] | SPP [{1-p_cp}]
    # CPP -> 'CPNoun' 'Adj1' CPVerb [{p_cp_short*0.5}] | 'CPNoun' 'Adj2' CPVerb [{p_cp_short*0.5}] | 'CPNoun' 'Adj1' 'Adj2' CPVerb [{(1-p_cp_short)*0.5}] | 'CPNoun' 'Adj2' 'Adj1' CPVerb [{(1-p_cp_short)*0.5}]
    # CPVerb -> 'LightVerb' [{p_cp_lightverb}] | 'OtherVerb' [{1-p_cp_lightverb}]
    # SPP -> 'SPNoun' 'Adj1' SPVerb [{p_sp_short*0.5}] | 'SPNoun' 'Adj2' SPVerb [{p_sp_short*0.5}] | 'SPNoun' 'Adj1' 'Adj2' SPVerb [{(1-p_sp_short)*0.5}] | 'SPNoun' 'Adj2' 'Adj1' SPVerb [{(1-p_cp_short)*0.5}]
    # SPVerb -> 'LightVerb' [{p_sp_lightverb}] | 'OtherVerb' [{1-p_sp_lightverb}]
    # """
    return f"""
    S -> CPP [{p_cp}] | SPP [{1-p_cp}]
    CPP -> 'CPNoun' CPIntv CPVerb [{p_cp_intv}] | 'CPNoun' CPVerb [{(1-p_cp_intv)}]
    CPIntv -> 'Adj1' [{p_cp_short*0.5}] | 'Adj2' [{p_cp_short*0.5}] | 'Adj1' 'Adj2' [{(1-p_cp_short)*0.5}] | 'Adj2' 'Adj1' [{(1-p_cp_short)*0.5}]
    CPVerb -> 'LightVerb' [{p_cp_lightverb}] | 'OtherVerb' [{1-p_cp_lightverb}]
    SPP -> 'SPNoun' SPIntv SPVerb [{p_sp_intv}] | 'SPNoun' SPVerb [{(1-p_sp_intv)}]
    SPIntv -> 'Adj1' [{p_sp_short*0.5}] | 'Adj2' [{p_sp_short*0.5}] | 'Adj1' 'Adj2' [{(1-p_sp_short)*0.5}] | 'Adj2' 'Adj1' [{(1-p_sp_short)*0.5}]
    SPVerb -> 'LightVerb' [{p_sp_lightverb}] | 'OtherVerb' [{1-p_sp_lightverb}]
    """
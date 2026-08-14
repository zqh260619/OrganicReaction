"""样式属性持有者 AttributeHolder 与默认属性 DEFAULT_ATTRIBUTES。"""

from manim import WHITE, ManimColor

from .parameters import bond_length, ratio_transition_state, edge, txt_size, default_charge_edge

class AttributeHolder:
    def __init__(self,*,
                 base_ratio_outbond:float,
                 base_ratio_inbond:float,
                 num_inbond:int,
                 dashed_length_dashedbond:float,
                 dashed_ratio_dashedbond:float,
                 ratio_transition_state_dashedbond:float,
                 length_global:float,
                 color:ManimColor,
                 edge_global:float,
                 font_size:float,
                 radius_negative:float,
                 ratio_negative:float,
                 stroke_width_negative:float,
                 edge_charge:float,
                 radius_positive:float,
                 ratio_positive:float,
                 stroke_width_positive:float,
                 radius_single:float,
                 distance_pair:float,
                 distance_double:float,
                 edge_ratio_double:float,
                 distance_triple:float):

        self.base_ratio_outbond=base_ratio_outbond
        self.base_ratio_inbond=base_ratio_inbond
        self.num_inbond=num_inbond
        self.dashed_length_dashedbond=dashed_length_dashedbond
        self.dashed_ratio_dashedbond=dashed_ratio_dashedbond
        self.ratio_transition_state_dashedbond=ratio_transition_state_dashedbond
        self.length_global=length_global
        self.color=color
        self.edge_global=edge_global
        self.font_size=font_size
        self.radius_negative=radius_negative
        self.ratio_negative=ratio_negative
        self.stroke_width_negative=stroke_width_negative
        self.edge_charge=edge_charge
        self.radius_positive=radius_positive
        self.ratio_positive=ratio_positive
        self.stroke_width_positive=stroke_width_positive
        self.radius_single=radius_single
        self.distance_pair=distance_pair
        self.distance_double=distance_double
        self.edge_ratio_double=edge_ratio_double
        self.distance_triple=distance_triple

#default settings
DEFAULT_ATTRIBUTES=AttributeHolder(base_ratio_outbond=0.2,
                                   base_ratio_inbond=0.2,
                                   num_inbond=5,
                                   dashed_length_dashedbond=0.1,
                                   dashed_ratio_dashedbond=0.5,
                                   ratio_transition_state_dashedbond=bond_length*ratio_transition_state,
                                   length_global=bond_length,
                                   color=WHITE,
                                   edge_global=edge,
                                   font_size=txt_size,
                                   radius_negative=0.05,
                                   ratio_negative=0.6,
                                   stroke_width_negative=1.2,
                                   edge_charge=default_charge_edge,
                                   radius_positive=0.05,
                                   ratio_positive=0.6,
                                   stroke_width_positive=1.2,
                                   radius_single=0.01,
                                   distance_pair=0.1,
                                   distance_double=0.12,
                                   edge_ratio_double=0.08,
                                   distance_triple=0.12)

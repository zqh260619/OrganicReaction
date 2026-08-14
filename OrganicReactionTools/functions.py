"""工具函数。"""

from manim import Scene, Animation, Mobject, ApplyMethod, turn_animation_into_updater, smooth
import numpy as np

from .parameters import RNG

#functions
def play_timeline(scene:Scene,timeline:dict[float,Animation]):

    # Inspired by github.com/abul4fia/manim-play-timeline's timeline implementation

    pretime=0
    ending=0
    for time,animation in sorted(timeline.items()):
        to_wait=time-pretime
        if to_wait>0:
            scene.wait(to_wait)
        pretime=time
        for anim in animation:
            turn_animation_into_updater(anim)
            scene.add(anim.mobject)
            ending=max(ending,anim.run_time+time)
    if ending>time:
        scene.wait(ending-pretime)

def merging_timeline(timeline1:dict[float,list[Animation]|Animation],timeline2:dict[float,list[Animation]|Animation]):
    rslt=timeline1.copy()
    for time,anims in timeline2.items():
        if time in rslt:
            if not isinstance(rslt[time],list):
                rslt[time]=[rslt[time]]
            if not isinstance(anims,list):
                anims=[anims]
            rslt[time].extend(anims)
        else:
            rslt[time]=anims
    return rslt

def brownian_motion(items:Mobject|list,num:int,time:float=1.0):
    if isinstance(items,list):
        temp={}
        for item in items:
            temp=merging_timeline(temp,brownian_motion(item,num,time))
        return temp
    else:
        node=[]
        while len(node)<num:
            temp_node=RNG.uniform(0,time)
            node.append(temp_node)
        node=sorted(node)
        node.append(time)

        rslt={}
        destination=items.get_center()
        for i in range(num):
            dx=np.array([RNG.uniform(-0.5,0.5),RNG.uniform(-0.5,0.5),0])
            destination+=dx
            if np.abs(destination[0])>5 or np.abs(destination[1])>3:
                destination[0]=destination[0]/7*6
                destination[1]=destination[1]/4*3
            if i == 0:
                rslt[0] = [ApplyMethod(
                    items.shift,
                    dx,
                    run_time=node[i],
                    rate_func=smooth)]
            else:
                rslt[node[i-1]] = [ApplyMethod(
                    items.shift,
                    dx,
                    run_time=node[i] - node[i-1],
                    rate_func=smooth)]
        return rslt

#!/usr/bin/env python

import functools
import py_trees
import py_trees_ros
import py_trees.console as console
import move_base_msgs
import geometry_msgs

import rospy
import sys



def create_root():
    pose1 = geometry_msgs.msg.PoseStamped()
    pose1.header.frame_id = "map"
    pose1.pose.position.x = 2.37806487083
    pose1.pose.position.y = -5.06126594543
    pose1.pose.orientation.z = -0.386511298043
    pose1.pose.orientation.w = 0.922284672151
    
    move1 = py_trees_ros.actions.ActionClient(
        name="Move1",
        action_namespace="/move_base",
        action_spec=move_base_msgs.msg.MoveBaseAction,
        action_goal=move_base_msgs.msg.MoveBaseGoal(target_pose=pose1)
    )

    pose2 = geometry_msgs.msg.PoseStamped()
    pose2.header.frame_id = "map"
    pose2.pose.position.x = 3.69893360138
    pose2.pose.position.y = -6.41148042679
    pose2.pose.orientation.z = -0.389941751738
    pose2.pose.orientation.w = 0.920839524701
    move2 = py_trees_ros.actions.ActionClient(
        name="Move2",
        action_namespace="/move_base",
        action_spec=move_base_msgs.msg.MoveBaseAction,
        action_goal=move_base_msgs.msg.MoveBaseGoal(target_pose=pose2)
    )
    
    moves = py_trees.composites.Sequence("Moves")

    root = py_trees.composites.Parallel("Tutorial")
    idle = py_trees.behaviours.Running(name="Idle")
    
    root.add_children([moves])
    moves.add_child(move1)
    moves.add_child(move2)
    moves.add_child(idle)
    return root


def shutdown(behaviour_tree):
    behaviour_tree.interrupt()

def main():
    rospy.init_node("tree")
    root = create_root()
    behaviour_tree = py_trees_ros.trees.BehaviourTree(root)
    rospy.on_shutdown(functools.partial(shutdown, behaviour_tree))
    if not behaviour_tree.setup(timeout=15):
        console.logerror("failed to setup the tree, aborting.")
        sys.exit(1)
    behaviour_tree.tick_tock(500)

    try:
        module_itself = importlib.import_module(module_name)
    except ImportError:
        console.logerror("Could not import module [{0}]".format(args.name))
        sys.exit(1)
   
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

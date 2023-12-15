import argparse
import pandas
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
from statannot import add_stat_annotation
import pprint
import os
import sys

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.stats import wilcoxon
from scipy.stats import mannwhitneyu

parser = argparse.ArgumentParser()
parser.add_argument("study")
parser.add_argument("experiments")
parser.add_argument("runs")
parser.add_argument("generations")
parser.add_argument("comparison")
parser.add_argument("mainpath")
args = parser.parse_args()

study = args.study
experiments_name = args.experiments.split(',')
runs = list(range(1, int(args.runs) + 1))
generations = list(map(int, args.generations.split(',')))
comparison = args.comparison
mainpath = args.mainpath

experiments = experiments_name
inner_metrics = ['mean', 'max']
include_max = False
merge_lines = True
gens_boxes = generations
clrs = ['#1f77b4',
        '#aec7e8',
        '#800000',
        '#d62728']
path = f'{mainpath}/{study}'

measures = {
    'speed_y': ['Speed (cm/s)', 0, 1]}


def plots():
    if not os.path.exists(f'{path}/analysis/{comparison}'):
        os.makedirs(f'{path}/analysis/{comparison}')

    df_outer = pandas.read_csv(f'{path}/analysis/df_outer.csv')
    df_inner = pandas.read_csv(f'{path}/analysis/df_inner.csv')

    #wilcoxon_test()
    #mannwhitneyu_test()
    perform_wilcoxon_tests(df_inner)
    #plot_ratio(df_outer)

    #plot_speed_joints(df_outer)
    #plot_3D(df_outer)
    #plot_3D_scatter(df_outer)
    #plot_3D_contour(df_outer)
    #plot_2D_contour(df_outer)


def perform_wilcoxon_tests(df_inner):
    tests_combinations = [(experiments[i], experiments[j])
                          for i in range(len(experiments)) for j in range(i + 1, len(experiments))]

    for gen_boxes in gens_boxes:
        df_inner2 = df_inner[(df_inner['generation_index'] == gen_boxes) & (df_inner['run'] <= max(runs))]

        for measure in measures.keys():
            print(f"Wilcoxon tests for {measure} at generation {gen_boxes}:\n")
            for exp1, exp2 in tests_combinations:
                data1 = df_inner2[df_inner2['experiment'] == exp1][f'{measure}_{inner_metrics[0]}']
                data2 = df_inner2[df_inner2['experiment'] == exp2][f'{measure}_{inner_metrics[0]}']

                _, p_value = wilcoxon(data1, data2)
                print(f"Comparison between {exp1} and {exp2}: p-value = {p_value}")
            print()  # Print an empty line for better readability between measures

def mannwhitneyu_test():

    ratios_speed = pandas.read_csv(f'{path}/analysis/ratio_speed.csv')
    earth_ratio = ratios_speed['earth_ratio']
    moon_ratio = ratios_speed['moon_ratio']

    # Perform Wilcoxon test
    statistic, p_value = mannwhitneyu(earth_ratio, moon_ratio)

    print(f"Mann-Whitney U Statistic: {statistic}")
    print(f"P-value: {p_value}")


def wilcoxon_test():

    ratios_speed = pandas.read_csv(f'{path}/analysis/ratio_speed.csv')
    earth_ratio = ratios_speed['earth_ratio']
    moon_ratio = ratios_speed['moon_ratio']

    # Perform Wilcoxon test
    statistic, p_value = wilcoxon(earth_ratio, moon_ratio)

    print(f"Wilcoxon Statistic: {statistic}")
    print(f"P-value: {p_value}")


def plot_speed_joints(df_outer):
    print('plotting lines...')

    font = {'font.size': 20}
    plt.rcParams.update(font)
    fig, ax = plt.subplots()

    plt.xlabel('')
    plt.ylabel('')

    speed_earth = df_outer[df_outer['experiment'] == experiments[0]][f'speed_y_{inner_metrics[0]}_median']
    joints_earth = df_outer[df_outer['experiment'] == experiments[0]][f'num_act_joints_{inner_metrics[0]}_median']

    speed_moon = df_outer[df_outer['experiment'] == experiments[1]][f'speed_y_{inner_metrics[0]}_median']
    joints_moon = df_outer[df_outer['experiment'] == experiments[1]][f'num_act_joints_{inner_metrics[0]}_median']

    speed_earth = speed_earth.reset_index(drop=True)
    speed_moon = speed_moon.reset_index(drop=True)
    joints_earth = joints_earth.reset_index(drop=True)
    joints_moon = joints_moon.reset_index(drop=True)


    ax.plot(df_outer[df_outer['experiment'] == experiments[0]]['generation_index'], speed_earth,
            label=f'Speed Earth', c=clrs[0])
    ax.plot(df_outer[df_outer['experiment'] == experiments[0]]['generation_index'], joints_earth,
            label=f'Active joints Earth', c=clrs[1])
    ax.plot(df_outer[df_outer['experiment'] == experiments[1]]['generation_index'], speed_moon,
            label=f'Speed Moon', c=clrs[2])
    ax.plot(df_outer[df_outer['experiment'] == experiments[1]]['generation_index'], joints_moon,
            label=f'Active joints Moon', c=clrs[3])

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5, fontsize=10)

    plt.savefig(f'{path}/analysis/{comparison}/speed_vs_act_joints.png', bbox_inches='tight')
    plt.clf()
    plt.close(fig)

    print('plotted lines!')


def plot_3D_scatter(df_outer):
    print('plotting scatter plot...')

    font = {'font.size': 17}
    plt.rcParams.update(font)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ratios_speed = pandas.read_csv(f'{path}/analysis/ratio_speed.csv')

    ax.set_xlabel('Generation Index')
    ax.set_zlabel('Ratio of Speed')
    ax.set_ylabel('Active Joints')

    # speed_earth = df_outer[df_outer['experiment'] == experiments[0]][f'speed_y_{inner_metrics[0]}_median']
    speed_earth = ratios_speed['earth_ratio']
    joints_earth = df_outer[df_outer['experiment'] == experiments[0]][f'num_act_joints_{inner_metrics[0]}_median']

    # speed_moon = df_outer[df_outer['experiment'] == experiments[1]][f'speed_y_{inner_metrics[0]}_median']
    speed_moon = ratios_speed['moon_ratio']
    joints_moon = df_outer[df_outer['experiment'] == experiments[1]][f'num_act_joints_{inner_metrics[0]}_median']

    gen_idx_earth = df_outer[df_outer['experiment'] == experiments[0]]['generation_index']
    gen_idx_moon = df_outer[df_outer['experiment'] == experiments[1]]['generation_index']

    ax.scatter(gen_idx_earth, joints_earth, speed_earth, label='Earth', c=clrs[0], marker='o')
    ax.scatter(gen_idx_moon, joints_moon, speed_moon, label='Moon', c=clrs[2], marker='o')

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5, fontsize=7)

    plt.savefig(f'{path}/analysis/{comparison}/speed_vs_joints_3d_scatter.png', bbox_inches='tight')
    plt.clf()
    plt.close(fig)


def plot_3D_contour(df_outer):
    print('plotting contour...')

    font = {'font.size': 17}
    plt.rcParams.update(font)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel('Generation Index')
    ax.set_ylabel('Ratio of Speed')
    ax.set_zlabel('Active Joints')

    speed_earth = df_outer[df_outer['experiment'] == experiments[0]][f'speed_y_{inner_metrics[0]}_median']
    joints_earth = df_outer[df_outer['experiment'] == experiments[0]][f'num_act_joints_{inner_metrics[0]}_median']

    speed_moon = df_outer[df_outer['experiment'] == experiments[1]][f'speed_y_{inner_metrics[0]}_median']
    joints_moon = df_outer[df_outer['experiment'] == experiments[1]][f'num_act_joints_{inner_metrics[0]}_median']

    gen_idx_earth = df_outer[df_outer['experiment'] == experiments[0]]['generation_index']
    gen_idx_moon = df_outer[df_outer['experiment'] == experiments[1]]['generation_index']

    # Creating a grid of gen_idx_earth and speed_earth
    gen_idx_grid, speed_grid = np.meshgrid(gen_idx_earth, speed_earth)

    # Reshaping joints_earth to match the dimensions of the grid
    joints_earth_2d = np.tile(joints_earth, (len(gen_idx_earth), 1))

    ax.plot(gen_idx_earth, speed_earth, zs=0, zdir='z', label='Earth', c='blue', marker='o')
    ax.plot(gen_idx_moon, speed_moon, zs=0, zdir='z', label='Moon', c='green', marker='o')

    ax.contour(gen_idx_grid, speed_grid, joints_earth_2d, zdir='z', offset=np.min(joints_earth), colors='blue',
               linewidths=2)

    # Similarly, plot contours for the Moon data if needed

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5, fontsize=10)

    plt.savefig(f'{path}/analysis/{comparison}/speed_vs_joints_3d_contour.png', bbox_inches='tight')
    plt.clf()
    plt.close(fig)


def plot_2D_contour(df_outer):
    print('plotting 2D contour...')

    font = {'font.size': 20}
    plt.rcParams.update(font)
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_xlabel('Generation Index')
    ax.set_ylabel('Speed')

    speed_earth = df_outer[df_outer['experiment'] == experiments[0]][f'speed_y_{inner_metrics[0]}_median']
    joints_earth = df_outer[df_outer['experiment'] == experiments[0]][f'num_act_joints_{inner_metrics[0]}_median']

    gen_idx_earth = df_outer[df_outer['experiment'] == experiments[0]]['generation_index']

    # Creating a grid of gen_idx_earth and speed_earth
    gen_idx_grid, speed_grid = np.meshgrid(gen_idx_earth, speed_earth)

    # Reshaping joints_earth to match the dimensions of the grid
    joints_earth_2d = np.tile(joints_earth, (len(gen_idx_earth), 1))

    # Plotting the contourf plot with different colors
    contour = ax.contourf(gen_idx_grid, speed_grid, joints_earth_2d, levels=20, cmap='viridis')
    cbar = fig.colorbar(contour)
    cbar.set_label('Active Joints')

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5, fontsize=10)

    plt.savefig(f'{path}/analysis/{comparison}/speed_vs_joints_2d_contour.png', bbox_inches='tight')
    plt.clf()
    plt.close(fig)

def plot_3D(df_outer):
    print('plotting lines...')

    font = {'font.size': 20}
    plt.rcParams.update(font)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel('Generation Index')
    ax.set_ylabel('Speed')
    ax.set_zlabel('Active Joints')

    speed_earth = df_outer[df_outer['experiment'] == experiments[0]][f'speed_y_{inner_metrics[0]}_median']
    joints_earth = df_outer[df_outer['experiment'] == experiments[0]][f'num_act_joints_{inner_metrics[0]}_median']

    speed_moon = df_outer[df_outer['experiment'] == experiments[1]][f'speed_y_{inner_metrics[0]}_median']
    joints_moon = df_outer[df_outer['experiment'] == experiments[1]][f'num_act_joints_{inner_metrics[0]}_median']

    gen_idx_earth = df_outer[df_outer['experiment'] == experiments[0]]['generation_index']
    gen_idx_moon = df_outer[df_outer['experiment'] == experiments[1]]['generation_index']

    ax.plot(gen_idx_earth, speed_earth, joints_earth, label='Earth', c='blue', marker='o')
    ax.plot(gen_idx_moon, speed_moon, joints_moon, label='Moon', c='green', marker='o')

    # Find the minimum values of joints_earth and joints_moon
    min_joints_earth = np.min(joints_earth)
    min_joints_moon = np.min(joints_moon)

    # Set z_bottom_earth and z_bottom_moon to be slightly below the minimum values
    z_bottom_earth = np.full_like(gen_idx_earth, min_joints_earth - 0.1)
    z_bottom_moon = np.full_like(gen_idx_moon, min_joints_moon - 0.1)

    # Filling between lines and 0 in the z-axis for Earth
    ax.plot(gen_idx_earth, speed_earth, z_bottom_earth, alpha=0)  # Plotting to create initial vertices for the surface
    ax.plot(gen_idx_earth, speed_earth, joints_earth, alpha=0)  # Hiding the line
    ax.plot_surface(np.array([gen_idx_earth, gen_idx_earth]),
                    np.array([speed_earth, speed_earth]),
                    np.array([z_bottom_earth, joints_earth]), color='blue', alpha=0.3)

    # Filling between lines and 0 in the z-axis for Moon
    ax.plot(gen_idx_moon, speed_moon, z_bottom_moon, alpha=0)  # Plotting to create initial vertices for the surface
    ax.plot(gen_idx_moon, speed_moon, joints_moon, alpha=0)  # Hiding the line
    ax.plot_surface(np.array([gen_idx_moon, gen_idx_moon]),
                    np.array([speed_moon, speed_moon]),
                    np.array([z_bottom_moon, joints_moon]), color='green', alpha=0.3)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5, fontsize=10)

    plt.savefig(f'{path}/analysis/{comparison}/speed_vs_joints_3d.png', bbox_inches='tight')
    plt.clf()
    plt.close(fig)

def plot_ratio(df_outer):
    print('plotting lines...')

    # min_max_outer(df_outer)
    for measure in measures.keys():

        font = {'font.size': 20}
        plt.rcParams.update(font)
        fig, ax = plt.subplots()

        plt.xlabel('')
        plt.ylabel(f'{measures[measure][0]}')

        earth = df_outer[df_outer['experiment'] == experiments[0]][f'{measure}_{inner_metrics[0]}_median']
        earth_block = df_outer[df_outer['experiment'] == experiments[1]][f'{measure}_{inner_metrics[0]}_median']
        moon = df_outer[df_outer['experiment'] == experiments[2]][f'{measure}_{inner_metrics[0]}_median']
        moon_blocked = df_outer[df_outer['experiment'] == experiments[3]][f'{measure}_{inner_metrics[0]}_median']

        earth_q25 = df_outer[df_outer['experiment'] == experiments[0]][f'{measure}_{inner_metrics[0]}_q25']
        earth_block_q25 = df_outer[df_outer['experiment'] == experiments[1]][f'{measure}_{inner_metrics[0]}_q25']
        moon_q25 = df_outer[df_outer['experiment'] == experiments[2]][f'{measure}_{inner_metrics[0]}_q25']
        moon_blocked_q25 = df_outer[df_outer['experiment'] == experiments[3]][f'{measure}_{inner_metrics[0]}_q25']

        earth_q75 = df_outer[df_outer['experiment'] == experiments[0]][f'{measure}_{inner_metrics[0]}_q75']
        earth_block_q75 = df_outer[df_outer['experiment'] == experiments[1]][f'{measure}_{inner_metrics[0]}_q75']
        moon_q75 = df_outer[df_outer['experiment'] == experiments[2]][f'{measure}_{inner_metrics[0]}_q75']
        moon_blocked_q75 = df_outer[df_outer['experiment'] == experiments[3]][f'{measure}_{inner_metrics[0]}_q75']

        earth = earth.reset_index(drop=True)
        earth_block = earth_block.reset_index(drop=True)
        moon = moon.reset_index(drop=True)
        moon_blocked = moon_blocked.reset_index(drop=True)

        earth_q25 = earth_q25.reset_index(drop=True)
        earth_block_q25 = earth_block_q25.reset_index(drop=True)
        moon_q25 = moon_q25.reset_index(drop=True)
        moon_blocked_q25 = moon_blocked_q25.reset_index(drop=True)

        earth_q75 = earth_q75.reset_index(drop=True)
        earth_block_q75 = earth_block_q75.reset_index(drop=True)
        moon_q75 = moon_q75.reset_index(drop=True)
        moon_blocked_q75 = moon_blocked_q75.reset_index(drop=True)

        ratio_df = pandas.DataFrame()

        earth_ratio = earth_block / earth
        moon_ratio = moon_blocked / moon

        earth_ratio_25 = earth_block_q25 / earth_q25
        moon_ratio_25 = moon_blocked_q25 / moon_q25

        earth_ratio_75 = earth_block_q75 / earth_q75
        moon_ratio_75 = moon_blocked_q75 / moon_q75

        ratio_df['earth_ratio'] = earth_ratio
        ratio_df['moon_ratio'] = moon_ratio

        ratio_df.to_csv(f'{path}/analysis/ratio_speed.csv')

        ax.plot(df_outer[df_outer['experiment'] == experiments[0]]['generation_index'], earth_ratio,
                label=f'Ratio Earth Individuals', c=clrs[0])
        ax.plot(df_outer[df_outer['experiment'] == experiments[2]]['generation_index'], moon_ratio,
                label=f'Ratio Moon Individuals', c=clrs[2])

        ax.fill_between(df_outer[df_outer['experiment'] == experiments[0]]['generation_index'],
                        earth_ratio_25, earth_ratio_75,
                        color=clrs[0], alpha=0.3)
        ax.fill_between(df_outer[df_outer['experiment'] == experiments[2]]['generation_index'],
                        moon_ratio_25, moon_ratio_75,
                        color=clrs[2], alpha=0.3)

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5, fontsize=10)

        plt.savefig(f'{path}/analysis/{comparison}/line_ratios_{measure}.png', bbox_inches='tight')
        plt.clf()
        plt.close(fig)

    print('plotted lines!')


def plot_over(df_outer):
    print('plotting lines...')

    # min_max_outer(df_outer)
    for measure in measures.keys():

        font = {'font.size': 20}
        plt.rcParams.update(font)
        fig, ax = plt.subplots()

        plt.xlabel('')
        plt.ylabel(f'{measures[measure][0]}')


        for i in range(len(experiments)):

            data = df_outer[(df_outer['experiment'] == experiments[i])]
            data_blocked = df_outer[(df_outer['experiment'] == experiments[i + 1])]

            data = data.reset_index(drop=True)
            data_blocked = data_blocked.reset_index(drop=True)

            ax.plot(data_blocked[f'{measure}_{inner_metrics[0]}_median'].div(data[f'{measure}_{inner_metrics[0]}_median']),
                    label=f'Proportion_{inner_metrics[0]}', c=clrs[i])

            ax.fill_between(data['generation_index'],
                            data_blocked[f'{measure}_{inner_metrics[0]}_q25']/data[f'{measure}_{inner_metrics[0]}_q25'],
                            data_blocked[f'{measure}_{inner_metrics[0]}_q75']/data[f'{measure}_{inner_metrics[0]}_q75'],
                            alpha=0.3, facecolor=clrs[i])

            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=5, fontsize=10)
            if not merge_lines:
                plt.savefig(f'{path}/analysis/{comparison}/line_{experiments[i]}_{measure}.png', bbox_inches='tight')
                plt.clf()
                plt.close(fig)
                plt.rcParams.update(font)
                fig, ax = plt.subplots()
            print("!!!!!", i)
            i += 1

        if merge_lines:
            plt.savefig(f'{path}/analysis/{comparison}/line_{measure}.png', bbox_inches='tight')
            plt.clf()
            plt.close(fig)

    print('plotted lines!')

plots()





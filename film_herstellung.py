import moviepy.video.io.ImageSequenceClip
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import time
import argparse
import sys
import re
import os
from pandas import DataFrame as df
from matplotlib import rc
from tqdm import tqdm

class Stellt_video:

    def __init__(self, pfad_2_d, ordner, pics):
        self.pics      = pics
        self.pfad_2_d  = pfad_2_d
        self.sim_n_ord = os.path.join(self.pfad_2_d, ordner)
        # FE-AF Ordner
        self.fe_af_o = os.path.join(self.pfad_2_d, ordner, "FE-AF")
        # FE-FE Ordner
        self.fe_fe_o = os.path.join(self.pfad_2_d, ordner, "FE-FE")
    
        # Lies Dateien (output alpha FE-AF)
        self.fe_af_oal = pd.read_csv(os.path.join(self.fe_af_o,
                                                  'out-alpha-sp-g.out'),
                                     delim_whitespace=True, dtype=float,
                                     names = ['Vg_a_fe_af', 'Energie',
                                              'DOS_a_fe_af', 'T_a_fe_af']) 
        # Lies Dateien (output beta FE-AF)
        self.fe_af_obe = pd.read_csv(os.path.join(self.fe_af_o,
                                                  'out-beta-sp-g.out'),
                                     delim_whitespace=True, dtype=float,
                                     names = ['Vg_b_fe_af', 'Energie_b_fe_af',
                                              'DOS_b_fe_af', 'T_b_fe_af']) 
        # Lies Dateien (output alpha FE-FE)
        self.fe_fe_oal = pd.read_csv(os.path.join(self.fe_fe_o,
                                                  'out-alpha-sp-g.out'),
                                     delim_whitespace=True, dtype=float,
                                     names = ['Vg_a_fe_fe', 'Energie_a_fe_fe',
                                              'DOS_a_fe_fe', 'T_a_fe_fe']) 
        # Lies Dateien (output beta FE-FE)
        self.fe_fe_obe = pd.read_csv(os.path.join(self.fe_fe_o,
                                                  'out-beta-sp-g.out'),
                                     delim_whitespace=True, dtype=float,
                                     names = ['Vg_b_fe_fe', 'Energie_b_fe_fe',
                                              'DOS_b_fe_fe', 'T_b_fe_fe']) 

        self.df_ovoll = df(pd.concat([self.fe_af_oal, self.fe_af_obe,
                                      self.fe_fe_oal, self.fe_fe_obe],
                                     axis=1))

        self.df_ovoll =self.df_ovoll.drop(columns = ['Vg_b_fe_af',
                                                     'Vg_a_fe_fe',
                                                     'Vg_b_fe_fe',
                                                     'Energie_b_fe_af',
                                                     'Energie_a_fe_fe',
                                                     'Energie_b_fe_fe'])

        try:
            os.mkdir(os.path.join(self.sim_n_ord, 'pics_T'))
            self.out_d_pic_T = os.path.join(self.sim_n_ord, 'pics_T')
            os.mkdir(os.path.join(self.sim_n_ord, 'pics_D'))
            self.out_d_pic_D = os.path.join(self.sim_n_ord, 'pics_D')
        except FileExistsError:
            self.out_d_pic_T = os.path.join(self.sim_n_ord, 'pics_T')
            self.out_d_pic_D = os.path.join(self.sim_n_ord, 'pics_D')
        else:
            pass

    def Make_pics_T(self):
        for i in tqdm(range(self.pics)):
            Vg = self.df_ovoll['Vg_a_fe_af'][i * 2000]
            # Bilder
            self.voll_plot, axs = plt.subplots(2)
            fe_af_a = sns.lineplot(ax = axs[0],
                         x = "Energie",
                         y = "T_a_fe_af",
                         data = self.df_ovoll[i * 2000 : 2000 * (i + 1)],
                         linewidth=2,
                         color='red',
                         label='\u03B1')
            fe_af_b = sns.lineplot(ax=axs[0],
                         x = "Energie",
                         y = "T_b_fe_af",
                         data = self.df_ovoll[i * 2000 : 2000 * (i + 1)],
                         linewidth=2,
                         color='blue',
                         label='\u03B2')
            fe_fe_a = sns.lineplot(ax = axs[1],
                         x = "Energie",
                         y = "T_a_fe_fe",
                         data = self.df_ovoll[i * 2000 : 2000 * (i + 1)],
                         linewidth=2,
                         color='red',
                         label='\u03B1')
            fe_fe_b = sns.lineplot(ax=axs[1],
                         x = "Energie",
                         y = "T_b_fe_fe",
                         data = self.df_ovoll[i * 2000 : 2000 * (i + 1)],
                         linewidth=2,
                         color='blue',
                         label='\u03B2')

            ### Legend Kette
            #fe_af_a.legend(loc = 'upper right',
            #               fontsize = 5,
            #               title_fontsize = 6,
            #               shadow = True,
            #               bbox_to_anchor= (1.13, 1),
            #               title = 'E^(1)_(\u03B1,1) = {: .3f}\n'
            #                       'E^(1)_(\u03B1,2) = {: .3f}\n'
            #                       'E^(2)_(\u03B1,1) = {: .3f}\n'
            #                       'E^(2)_(\u03B1,2) = {: .3f}\n'
            #                       'Vg = {: .3f}'
            #                       .format(-0.26 - Vg, 0.26 - Vg,
            #                               -0.26 - Vg, 0.26 - Vg,
            #                               Vg))
            #fe_fe_b.legend(loc = 'upper right',
            #               fontsize = 6,
            #               title_fontsize = 7,
            #               shadow = True,
            #               bbox_to_anchor= (1.13, 1),
            #               title = 'E^(1)_(\u03B1,1) = {: .3f}\n'
            #                       'E^(1)_(\u03B1,2) = {: .3f}\n'
            #                       'E^(2)_(\u03B1,1) = {: .3f}\n'
            #                       'E^(2)_(\u03B1,2) = {: .3f}'\
            #                       .format(-0.26 - Vg, 0.26 - Vg,
            #                               -0.26 - Vg, 0.26 - Vg))

            ### Legend SMMs
            #fe_af_a.legend(loc = 'upper right',
            #               fontsize = 5,
            #               title_fontsize = 6,
            #               shadow = True,
            #               bbox_to_anchor= (1.13, 1),
            #               title = '\u03F5^(3)_(\u03B1,1) = {: .3f} \n'
            #                       '\u03F5^(3)_(\u03B1,2) = {: .3f} \n'
            #                       '\u03F5^(4)_(\u03B1,1) = {: .3f} \n'
            #                       '\u03F5^(4)_(\u03B1,2) = {: .3f} \n'
            #                       'Vg = {: .3f}'\
            #                       .format(-0.17 - Vg, 0.3 - Vg,
            #                                0.10 - Vg, 0.3 - Vg,
            #                                Vg))
            #fe_fe_b.legend(loc = 'upper right',
            #               fontsize = 6,
            #               title_fontsize = 7,
            #               shadow = True,
            #               bbox_to_anchor= (1.13, 1),
            #               title = '\u03F5^(3)_(\u03B1,1) = {: .3f} \n'
            #                       '\u03F5^(3)_(\u03B1,2) = {: .3f} \n'
            #                       '\u03F5^(4)_(\u03B1,1) = {: .3f} \n'
            #                       '\u03F5^(4)_(\u03B1,2) = {: .3f}'\
            #                       .format(-0.17 - Vg, 0.3 - Vg,
            #                               -0.17 - Vg, 0.3 - Vg))

            ### Legend Vg
            fe_af_a.legend(loc = 'upper right',
                           fontsize = 5,
                           title_fontsize = 6,
                           shadow = True,
                           bbox_to_anchor= (1.13, 1),
                           title = 'Vg = {: .3f}'.format(Vg))
            fe_fe_a.legend(loc = 'upper right',
                           fontsize = 5,
                           title_fontsize = 6,
                           shadow = True,
                           bbox_to_anchor= (1.13, 1),
                           title = 'Vg = {: .3f}'.format(Vg))

            axs[0].set(xlabel = ' ')
            axs[0].set(ylabel = 'T(arb. units)')
            axs[0].set_xlim((-0.2, 0.2))
            axs[0].set_ylim((0, 1))
            axs[1].set(xlabel = 'Energy (eV)')
            axs[1].set(ylabel = 'T(arb. units)')
            axs[1].set_xlim((-0.2, 0.2))
            axs[1].set_ylim((0,1))

            self.voll_plot.figure.savefig(os.path.join(self.out_d_pic_T,
                                               'picT0'+str(i)+'.png'), dpi=300)

    def Make_pics_D(self):
        for i in tqdm(range(self.pics)):
            Vg = self.df_ovoll['Vg_a_fe_af'][i * 2000]
            # Bilder
            self.voll_plot, axs = plt.subplots(2)
            fe_af_a = sns.lineplot(ax = axs[0],
                         x = "Energie",
                         y = "DOS_a_fe_af",
                         data = self.df_ovoll[i * 2000 : 2000 * (i + 1)],
                         linewidth=2,
                         color='red',
                         label='\u03B1')
            fe_af_b = sns.lineplot(ax=axs[0],
                         y = "DOS_b_fe_af",
                         x = "Energie",
                         data = self.df_ovoll[i * 2000 : 2000 * (i + 1)],
                         linewidth=2,
                         color='blue',
                         label='\u03B2')
            fe_fe_a = sns.lineplot(ax = axs[1],
                         x = "Energie",
                         y = "DOS_a_fe_fe",
                         data = self.df_ovoll[i * 2000 : 2000 * (i + 1)],
                         linewidth=2,
                         color='red',
                         label='\u03B1')
            fe_fe_b = sns.lineplot(ax=axs[1],
                         x = "Energie",
                         y = "DOS_b_fe_fe",
                         data = self.df_ovoll[i * 2000 : 2000 * (i + 1)],
                         linewidth=2,
                         color='blue',
                         label='\u03B2')

            l_fe_af_a = fe_af_a.lines[0]
            x_fe_af_a = l_fe_af_a.get_xydata()[:,0]
            y_fe_af_a = l_fe_af_a.get_xydata()[:,1]
            fe_af_a.fill_between(x_fe_af_a, y_fe_af_a, color="red", alpha=0.3)

            l_fe_af_b = fe_af_b.lines[1]
            x_fe_af_b = l_fe_af_b.get_xydata()[:,0]
            y_fe_af_b = l_fe_af_b.get_xydata()[:,1]
            fe_af_b.fill_between(x_fe_af_b, y_fe_af_b, color="blue", alpha=0.3)

            l_fe_fe_a = fe_fe_a.lines[0]
            x_fe_fe_a = l_fe_fe_a.get_xydata()[:,0]
            y_fe_fe_a = l_fe_fe_a.get_xydata()[:,1]
            fe_fe_a.fill_between(x_fe_fe_a, y_fe_fe_a, color="red", alpha=0.3)

            l_fe_fe_b = fe_fe_b.lines[1]
            x_fe_fe_b = l_fe_fe_b.get_xydata()[:,0]
            y_fe_fe_b = l_fe_fe_b.get_xydata()[:,1]
            fe_fe_b.fill_between(x_fe_fe_b, y_fe_fe_b, color="blue", alpha=0.3)

            ### Legend Vg
            fe_af_a.legend(loc = 'upper right',
                           fontsize = 5,
                           title_fontsize = 6,
                           shadow = True,
                           bbox_to_anchor= (1.13, 1),
                           title = 'Vg = {: .3f}'.format(Vg))
            fe_fe_a.legend(loc = 'upper right',
                           fontsize = 5,
                           title_fontsize = 6,
                           shadow = True,
                           bbox_to_anchor= (1.13, 1),
                           title = 'Vg = {: .3f}'.format(Vg))

            axs[0].set(xlabel = ' ')
            axs[0].set(ylabel = 'DOS(eV^{-1})')
            axs[0].set_xlim((-0.2, 0.2))
            axs[0].set_ylim((0.0, 50))
            axs[1].set(xlabel = 'Energy (eV)')
            axs[1].set(ylabel = 'DOS(eV^{-1})')
            axs[1].set_xlim((-0.2, 0.2))
            axs[1].set_ylim((0.0, 50))

            self.voll_plot.figure.savefig(os.path.join(self.out_d_pic_D,
                                               'picD0'+str(i)+'.png'), dpi=300)

    def Make_vid_T(self):
        fps = 12

        # Video
        bild = os.listdir(self.out_d_pic_T)
        bild.sort(key=lambda f: int(re.sub('\D', '', f)))

        bild_datei = [self.out_d_pic_T + '/' + img for img in bild]

        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(bild_datei,
                                                                    fps=fps)
        clip.write_videofile(os.path.join(self.sim_n_ord , 'Toy_modell_T.mp4'))

    def Make_vid_D(self):
        fps = 12

        # Video
        bild = os.listdir(self.out_d_pic_D)
        bild.sort(key=lambda f: int(re.sub('\D', '', f)))

        bild_datei = [self.out_d_pic_D + '/' + img for img in bild]

        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(bild_datei,
                                                                    fps=fps)
        clip.write_videofile(os.path.join(self.sim_n_ord , 'Toy_modell_D.mp4'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', help='Eingabe Ordner')
    parser.add_argument('-pt', '--pics_t', help='Menge von Bilder zu nutzen.'
                                                'Transmission')
    parser.add_argument('-pd', '--pics_d', help='Menge von Bilder zu nutzen.'
                                                'DOS')
    parser.add_argument('-vt', '--video_t', help='Stellen ein Video her.'
                                               'Transmission')
    parser.add_argument('-vd', '--video_d', help='Stellen ein Video her. DOS')


    args = parser.parse_args()

    if args.input != None:
        if args.pics_t != None and args.pics_d == None:
            pfad_2_d = os.path.dirname(os.path.abspath(args.input))
            stelltes_vid = Stellt_video(pfad_2_d, args.input, int(args.pics_t))
            stelltes_vid.Make_pics_T()

        elif args.pics_d != None and args.pics_t == None:
            pfad_2_d = os.path.dirname(os.path.abspath(args.input))
            stelltes_vid = Stellt_video(pfad_2_d, args.input, int(args.pics_d))
            stelltes_vid.Make_pics_D()
    
        elif args.video_t != None and args.video_d == None:
            pfad_2_d = os.path.dirname(os.path.abspath(args.input))
            stelltes_vid = Stellt_video(pfad_2_d, args.input, 1)
            stelltes_vid.Make_vid_T()
        elif args.video_d != None and args.video_t == None:
            pfad_2_d = os.path.dirname(os.path.abspath(args.input))
            stelltes_vid = Stellt_video(pfad_2_d, args.input, 1)
            stelltes_vid.Make_vid_D()

    else:
        print ('Fehler: Geben Sie bitte eine Eingabe')

import moviepy.video.io.ImageSequenceClip
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns
import pandas as pd
import numpy as np
import argparse
import sys
import re
import os
from pandas import DataFrame as df


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
            self.out_d_pic = os.mkdir(os.path.join(self.sim_n_ord, 'pics'))
        except FileExistsError:
            self.out_d_pic = os.path.join(self.sim_n_ord, 'pics')
        else:
            pass

    def Make_pics(self):


        for i in range(self.pics):
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

            #fe_af_a.legend(loc = 'upper right',
            #               fontsize = 5,
            #               title_fontsize = 6,
            #               shadow = True,
            #               bbox_to_anchor= (1.13, 1),
            #               title = 'E^(1)_(\u03B1,1) = {:.3f} \n'
            #                       'E^(2)_(\u03B1,1) = {:.3f}'\
            #                       .format(-0.26 - Vg, 0.26 - Vg))
            #fe_fe_b.legend(loc = 'upper right',
            #               fontsize = 6,
            #               title_fontsize = 7,
            #               shadow = True,
            #               bbox_to_anchor= (1.13, 1),
            #               title = 'E^(1)_(\u03B1,1) = {:.3f} \n'
            #                       'E^(2)_(\u03B1,1) = {:.3f}'\
            #                       .format(-0.26 - Vg, 0.26 - Vg))

            fe_af_a.legend(loc = 'upper right',
                           fontsize = 5,
                           title_fontsize = 6,
                           shadow = True,
                           bbox_to_anchor= (1.13, 1),
                           title = '\u03F5^(3)_(\u03B1,1) = {:.3f} \n'
                                   '\u03F5^(3)_(\u03B1,2) = {:.3f} \n'
                                   '\u03F5^(4)_(\u03B1,1) = {:.3f} \n'
                                   '\u03F5^(4)_(\u03B1,2) = {:.3f}'\
                                   .format(-0.17 - Vg, 0.3 - Vg, -0.17 - Vg, 0.1 - Vg))
            fe_fe_b.legend(loc = 'upper right',
                           fontsize = 6,
                           title_fontsize = 7,
                           shadow = True,
                           bbox_to_anchor= (1.13, 1),
                           title = '\u03F5^(3)_(\u03B1,1) = {:.3f} \n'
                                   '\u03F5^(3)_(\u03B1,2) = {:.3f} \n'
                                   '\u03F5^(4)_(\u03B1,1) = {:.3f} \n'
                                   '\u03F5^(4)_(\u03B1,2) = {:.3f}'\
                                   .format(-0.17 - Vg, 0.3 - Vg, -0.17 - Vg, 0.3 - Vg))

            axs[0].set(xlabel = ' ')
            axs[0].set(ylabel = 'T(arb. units)')
            axs[0].set_xlim((-0.5, 0.5))
            axs[0].set_ylim((0, 1))
            axs[1].set(xlabel = 'Energy (eV)')
            axs[1].set(ylabel = 'T(arb. units)')
            axs[1].set_xlim((-0.5, 0.5))
            axs[1].set_ylim((0,1))

            self.voll_plot.figure.savefig(os.path.join(self.out_d_pic,
                                               'pic0'+str(i)+'.png'), dpi=300)

    def Make_vid(self):
        fps = 12

        # Video
        bild = os.listdir(self.out_d_pic)
        bild.sort(key=lambda f: int(re.sub('\D', '', f)))

        bild_datei = [self.out_d_pic + '/' + img for img in bild]

        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(bild_datei, fps=fps)
        clip.write_videofile(os.path.join(self.sim_n_ord , 'Toy_modell.mp4'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input', help='Eingabe Ordner')
    parser.add_argument('-p', '--pics', help='Menge von Bilder zu nutzen')
    parser.add_argument('-v', '--video', help='Stellen ein Video her')


    args = parser.parse_args()

    if args.pics == None:
        args.pics = 1
    else:
        pass

    if args.input != None and args.video == None:
        pfad_2_d = os.path.dirname(os.path.abspath(args.input))
        stelltes_vid = Stellt_video(pfad_2_d, args.input, int(args.pics))
        stelltes_vid.Make_pics()

    elif args.input != None and args.video == 'ja':
        pfad_2_d = os.path.dirname(os.path.abspath(args.input))
        stelltes_vid = Stellt_video(pfad_2_d, args.input, int(args.pics))
        stelltes_vid.Make_vid()

    else:
        print ('Fehler: Geben Sie bitte eine Eingabe')

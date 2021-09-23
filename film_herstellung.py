import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys
import re
import os
from pandas import DataFrame as df
import moviepy.video.io.ImageSequenceClip


class Stellt_video:

    def __init__(self, pfad_2_d, ordner, pics):
        self.pics = pics
        self.pfad_2_d = pfad_2_d
        # FE-AF Ordner
        self.fe_af_o = os.path.join(self.pfad_2_d, ordner, "FE-AF")
        # FE-FE Ordner
        self.fe_fe_o = os.path.join(self.pfad_2_d, ordner, "FE-FE")
    
        # Lies Dateien (output alpha FE-AF)
        self.fe_af_oal = pd.read_csv(os.path.join(self.fe_af_o,
                                                  'out-alpha-sp-g.out'),
                                     delim_whitespace=True, dtype=float,
                                     names = ['Vg_a_fe_af', 'Energie_a_fe_af',
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

        print (self.df_ovoll)
        self.df_ovoll =self.df_ovoll.drop(columns = ['Vg_a_fe_af',
                                                     'Vg_b_fe_af',
                                                     'Vg_a_fe_fe',
                                                     'Vg_b_fe_fe'])
        print (self.df_ovoll)

    
        self.out_d_fe_af = os.path.join(self.fe_af_o, 'pics')
        self.out_d_fe_fe = os.path.join(self.fe_fe_o, 'pics')

    def Make_pics(self):
        try:
            self.out_d_fe_af = os.mkdir(os.path.join(self.fe_af_o, 'pics'))
            self.out_d_fe_fe = os.mkdir(os.path.join(self.fe_fe_o, 'pics'))
        except FileExistsError:
            self.out_d_fe_af = os.path.join(self.fe_af_o, 'pics')
            self.out_d_fe_fe = os.path.join(self.fe_fe_o, 'pics')
        else:
            pass

        for i in range(self.pics):
            # Bilder fuer FE-AF Zustand
            self.voll_plot, axs = plt.subplots(2)
            sns.lineplot(ax = axs[0],
                         x = "Energie_a_fe_af",
                         y = "T_a_fe_af",
                         data = self.df_ovoll[i * 2000 : 2000 * (i + 1)],
                         linewidth=2, color='red')
            sns.lineplot(ax=axs[0],
                         x = "Energie_b_fe_af",
                         y = "T_b_fe_af",
                         data = self.df_ovoll[i * 2000 : 2000 * (i + 1)],
                         linewidth=2, color='blue')
            sns.lineplot(ax = axs[1],
                         x = "Energie_a_fe_fe",
                         y = "T_a_fe_fe",
                         data = self.df_ovoll[i * 2000 : 2000 * (i + 1)],
                         linewidth=2, color='red')
            sns.lineplot(ax=axs[1],
                         x = "Energie_b_fe_fe",
                         y = "T_b_fe_fe",
                         data = self.df_ovoll[i * 2000 : 2000 * (i + 1)],
                         linewidth=2, color='blue')

            axs[0].set(xlabel = ' ')
            axs[0].set(ylabel = 'T(arb. units)')
            axs[0].set_xlim((-0.5, 0.5))
            axs[0].set_ylim((0, 1))
            axs[1].set(xlabel = 'Energy (eV)')
            axs[1].set(ylabel = 'T(arb. units)')
            axs[1].set_xlim((-0.5, 0.5))
            axs[1].set_ylim((0,1))

            #self.fe_af_oal_plot = sns.lineplot(x = "Energie_a_fe_af", y = "T_a_fe_af",
            #                                   data = self.df_ovoll[i*2000:
            #                                                         2000*(i+1)],
            #                              linewidth=2, color='red')
            #self.fe_af_oal_plot = sns.lineplot(x = "Energie_b_fe_af", y = "T_b_fe_af",
            #                                   data = self.df_ovoll[i*2000:
            #                                                         2000*(i+1)],
            #                              linewidth=2, color='blue')
    
            #self.fe_af_oal_plot.set_xlabel('Energy (eV)')
            #self.fe_af_oal_plot.set_ylabel('T (arb. units)')
            #self.fe_af_oal_plot.set_xlim(-0.5,0.5)
            #self.fe_af_oal_plot.set_ylim(0,1)
            #self.fe_af_oal_plot.figure.savefig(os.path.join(self.out_d_fe_af,
            #                                   'test_seaborn0'+str(i)+'.png'), dpi=300)
            self.voll_plot.figure.savefig(os.path.join(self.out_d_fe_af,
                                               'test_seaborn0'+str(i)+'.png'), dpi=300)
            #plt(self.voll_plot.figure)
            #self.fe_af_oal_plot.figure.clf()

            # Bilder fuer FE-FE Zustand
            #self.fe_fe_oal_plot = sns.lineplot(x = "Energie_a_fe_fe", y = "T_a_fe_fe",
            #                                   data = self.df_ovoll[i*2000:
            #                                                         2000*(i+1)],
            #                              linewidth=2, color='red')
            #self.fe_fe_oal_plot = sns.lineplot(x = "Energie_b_fe_fe", y = "T_b_fe_fe",
            #                                   data = self.df_ovoll[i*2000:
            #                                                         2000*(i+1)],
            #                              linewidth=2, color='blue')
    
            #self.fe_fe_oal_plot.set_xlabel('Energy (eV)')
            #self.fe_fe_oal_plot.set_ylabel('T (arb. units)')
            #self.fe_fe_oal_plot.set_xlim(-0.5,0.5)
            #self.fe_fe_oal_plot.set_ylim(0,1)
            #sns.set(font_scale = 1)
            #self.fe_fe_oal_plot.figure.savefig(os.path.join(self.out_d_fe_fe,
            #                                   'test_seaborn0'+str(i)+'.png'), dpi=300)
            #self.fe_fe_oal_plot.figure.clf()

    def Make_vid(self):
        fps = 12

        # Video fuer FE-AF Zustand
        bild    = os.listdir(self.out_d_fe_af)
        bild.sort(key=lambda f: int(re.sub('\D', '', f)))

        bild_datei = [self.out_d_fe_af + '/' + img for img in bild]

        clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(bild_datei, fps=fps)
        clip.write_videofile(os.path.join(self.fe_af_o, 'Toy_modelle.mp4'))

        # Video fuer FE-FE Zustand
        #bild    = os.listdir(self.out_d_fe_fe)
        #bild.sort(key=lambda f: int(re.sub('\D', '', f)))

        #bild_datei = [self.out_d_fe_fe + '/' + img for img in bild]

        #clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(bild_datei, fps=fps)
        #clip.write_videofile(os.path.join(self.fe_fe_o, 'Toy_modelle.mp4'))

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

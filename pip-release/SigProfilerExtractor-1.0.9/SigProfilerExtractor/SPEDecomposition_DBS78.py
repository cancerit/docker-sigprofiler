#!/usr/bin/env python3
"""
Created: February 21, 2020
@author: Mark Barnes
"""
import sys
import csv
import re
import os
import shutil
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import Image
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import piebar_figures as pie_figs

# Page Formatting
inch = 72
# USING LETTER LANDSCAPE DIMENSIONS
WIDTH_LETTER = 11 * inch
HEIGHT_LETTER = 8.5 * inch
MID_WIDTH_LETTER = 396
MID_HEIGHT_LETTER = HEIGHT_LETTER/2

WIDTH_GRAPH = 375
HEIGHT_GRAPH = 85

# Layout Formatting
HEIGHT_GAP = 93
WIDTH_GAP = 6
X_COORD = 0
Y_COORD = 1

# Coordinates for graphs on right side of plot
GRAPH_X_COORD = (WIDTH_LETTER) - WIDTH_GRAPH
GRAPH_Y_COORD = (HEIGHT_LETTER - HEIGHT_GAP)
TEXT_X_COORD = GRAPH_X_COORD + 55
TEXT_Y_COORD = (HEIGHT_LETTER - HEIGHT_GAP) + 63.75

pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

# Pairs are (x-coordinate, y-coordinate)
LAYOUT_5_GRAPH = [
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 1) + 10),
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 2) + 5),
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 3)),
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 4) - 5),
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 5) - 10)]

LAYOUT_5_TEXT = [
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 1) + 10),
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 2) + 5),
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 3)),
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 4) - 5),
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 5) - 10)]


LAYOUT_4_GRAPH = [
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 1) - HEIGHT_GRAPH/2 + 10),
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 2) - HEIGHT_GRAPH/2 + 5),
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 3) - HEIGHT_GRAPH/2 - 5),
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 4) - HEIGHT_GRAPH/2 - 10)]

LAYOUT_4_TEXT = [
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 1)- HEIGHT_GRAPH/2 + 10),
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 2)- HEIGHT_GRAPH/2 + 5),
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 3)- HEIGHT_GRAPH/2 - 5),
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 4)- HEIGHT_GRAPH/2 - 10)]


LAYOUT_3_GRAPH = [
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 2) + 5),
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 3)),
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 4) - 5)]

LAYOUT_3_TEXT = [
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 2) + 5),
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 3)),
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 4) - 5)]


LAYOUT_2_GRAPH = [
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 2) - HEIGHT_GRAPH/2 + 5),
(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 3) - HEIGHT_GRAPH/2 - 5)]

LAYOUT_2_TEXT = [
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 2)- HEIGHT_GRAPH/2 + 5),
(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 3)- HEIGHT_GRAPH/2 - 5)]


LAYOUT_1_GRAPH = [(GRAPH_X_COORD - WIDTH_GAP, (GRAPH_Y_COORD - HEIGHT_GRAPH * 3))]

LAYOUT_1_TEXT = [(TEXT_X_COORD, (TEXT_Y_COORD - HEIGHT_GRAPH * 3))]

LAYOUTS = [(LAYOUT_1_GRAPH,LAYOUT_1_TEXT), (LAYOUT_2_GRAPH, LAYOUT_2_TEXT),
(LAYOUT_3_GRAPH,LAYOUT_3_TEXT),(LAYOUT_4_GRAPH, LAYOUT_4_TEXT), (LAYOUT_5_GRAPH, LAYOUT_5_TEXT)]

PLOT_NAME = 0
CONTRIBUTION = 1


comparison_file_name = "comparison_with_global_ID_signatures.csv"
dir_cosmic = "cosmic_and_denovo_pngs/SPExtractor_DBS78_Cosmic_png/"
dir_signature = "cosmic_and_denovo_pngs/SPExtractor_DBS78_Signature_png/"

# Input: Cell w/ de_novo signatures decomposition signatures
# Output: Pair (name of plot, contribution)
def glob_nmf_parse(sig_name):

    if "DINUC-" in sig_name:
        dash_index = sig_name.index("-")
        plot_name = "DBS78" + sig_name[dash_index+1:]
        return (plot_name, "100%")
    else:
        sig_name = sig_name.strip(" ")
        o_bracket = sig_name.index("(") + 1
        c_bracket = sig_name.index(")")
        contribution = sig_name[o_bracket:c_bracket]
        plot_name = sig_name[10:o_bracket-2]
        return (plot_name, contribution)

# input format: "Signature 1536-A"
# output format: "SBS1536A"
def de_novo_parse(sig_name):
    #nine_index = sig_name.index("9")
    dash_index = sig_name.index("-")

    result = "DBS78" + sig_name[dash_index+1:]
    return result

# Helper functions for plotting the layout of a graph with 1-5 basis signatures
# Parameters:
#   de_novo_sig - (List) The de_novo_signature
#   basis_sigs - (List) The basis signatures
#   c_draw - (Canvas) The canvas for drawing the graph decomposition
def plot_1(de_novo_sig, basis_sigs, prefix, c_draw):
    for i in range(0,1):
        if "DBS78" in basis_sigs[i][0]:
            c_draw.drawImage(prefix+dir_signature+basis_sigs[i][0]+".png", LAYOUT_1_GRAPH[i][X_COORD], LAYOUT_1_GRAPH[i][Y_COORD], width=WIDTH_GRAPH, height=HEIGHT_GRAPH)
        else:
            c_draw.drawImage(prefix+dir_cosmic+basis_sigs[i][0]+".png", LAYOUT_1_GRAPH[i][X_COORD], LAYOUT_1_GRAPH[i][Y_COORD], width=WIDTH_GRAPH, height=HEIGHT_GRAPH)

        c_draw.drawString(LAYOUT_1_TEXT[i][X_COORD], LAYOUT_1_TEXT[i][Y_COORD], "contributes: " + str(basis_sigs[i][1]))

# Helper function for plotting the layout of a graph with 2 basis signatures
def plot_2(de_novo_sig, basis_sigs, prefix, c_draw):
    for i in range(0,2):
        if "DBS78" in basis_sigs[i][0]:
            c_draw.drawImage(prefix+dir_signature+basis_sigs[i][0]+".png", LAYOUT_2_GRAPH[i][X_COORD], LAYOUT_2_GRAPH[i][Y_COORD], width=WIDTH_GRAPH, height=HEIGHT_GRAPH)
        else:
            c_draw.drawImage(prefix+dir_cosmic+basis_sigs[i][0]+".png", LAYOUT_2_GRAPH[i][X_COORD], LAYOUT_2_GRAPH[i][Y_COORD], width=WIDTH_GRAPH, height=HEIGHT_GRAPH)
        c_draw.drawString(LAYOUT_2_TEXT[i][X_COORD], LAYOUT_2_TEXT[i][Y_COORD], "contributes: " + str(basis_sigs[i][1]))

# Helper function for plotting the layout of a graph with 3 basis signatures
def plot_3(de_novo_sig, basis_sigs, prefix, c_draw):
    for i in range(0,3):
        if "DBS78" in basis_sigs[i][0]:
            c_draw.drawImage(prefix+dir_signature+basis_sigs[i][0]+".png", LAYOUT_3_GRAPH[i][X_COORD], LAYOUT_3_GRAPH[i][Y_COORD], width=WIDTH_GRAPH, height=HEIGHT_GRAPH)
        else:
            c_draw.drawImage(prefix+dir_cosmic+basis_sigs[i][0]+".png", LAYOUT_3_GRAPH[i][X_COORD], LAYOUT_3_GRAPH[i][Y_COORD], width=WIDTH_GRAPH, height=HEIGHT_GRAPH)

        c_draw.drawString(LAYOUT_3_TEXT[i][X_COORD], LAYOUT_3_TEXT[i][Y_COORD], "contributes: " + str(basis_sigs[i][1]))

# Helper function for plotting the layout of a graph with 4 basis signatures
def plot_4(de_novo_sig, basis_sigs, prefix, c_draw):
    for i in range(0,4):
        if "DBS78" in basis_sigs[i][0]:
            c_draw.drawImage(prefix+dir_signature+basis_sigs[i][0]+".png",  \
             LAYOUT_4_GRAPH[i][X_COORD], LAYOUT_4_GRAPH[i][Y_COORD],        \
             width=WIDTH_GRAPH, height=HEIGHT_GRAPH)
        else:
            c_draw.drawImage(prefix+dir_cosmic+basis_sigs[i][0]+".png", LAYOUT_4_GRAPH[i][X_COORD], LAYOUT_4_GRAPH[i][Y_COORD], width=WIDTH_GRAPH, height=HEIGHT_GRAPH)
        c_draw.drawString(LAYOUT_4_TEXT[i][X_COORD], LAYOUT_4_TEXT[i][Y_COORD], "contributes: " + str(basis_sigs[i][1]))

# Helper function for plotting the layout of a graph with 5 basis signatures
def plot_5(de_novo_sig, basis_sigs, prefix, c_draw):
    for i in range(0,5):
        if "DBS78" in basis_sigs[i][0]:
            c_draw.drawImage(prefix+dir_signature+basis_sigs[i][0]+".png", LAYOUT_5_GRAPH[i][X_COORD], LAYOUT_5_GRAPH[i][Y_COORD], width=WIDTH_GRAPH, height=HEIGHT_GRAPH)
        else:
            c_draw.drawImage(prefix+dir_cosmic+basis_sigs[i][0]+".png", LAYOUT_5_GRAPH[i][X_COORD], LAYOUT_5_GRAPH[i][Y_COORD], width=WIDTH_GRAPH, height=HEIGHT_GRAPH)
        c_draw.drawString(LAYOUT_5_TEXT[i][X_COORD], LAYOUT_5_TEXT[i][Y_COORD], "contributes: " + str(basis_sigs[i][1]))

# Parameters:
#   de_novo - A string of the name of the de_novo signature that will match .jpg graph name
#   bases - A list of basis signatures from the COSMIC database that compose the de_novo signatures
#
# Output:
#   A graph of the de_novo signature's decomposition.
def gen_plot(de_novo, bases, cos_similarity, prefix, c):

    # to prevent the legend from distorting, we need to adjust the height dimensions
    legend_dims = [.25 * inch, .5 * inch, .65 * inch, .9 * inch, 1.05 * inch]
    num_extracted = len(bases)-1

    # THIS IS THE LEFT SIDE, IT DOES NOT CHANGE POSITION
    if "DBS78" in de_novo:
        c.drawImage(prefix+dir_signature+de_novo+ ".png", WIDTH_GAP, MID_HEIGHT_LETTER - (HEIGHT_GRAPH/2), width=WIDTH_GRAPH, height=HEIGHT_GRAPH)
    else:
        c.drawImage(prefix+dir_cosmic+de_novo+ ".png", WIDTH_GAP, MID_HEIGHT_LETTER - HEIGHT_GRAPH/2, width=WIDTH_GRAPH, height=HEIGHT_GRAPH)

    c.drawString(285, MID_HEIGHT_LETTER - 55, "Cosine Similarity: " + str(cos_similarity))
    c.drawImage(prefix+dir_signature+de_novo+"_bar.png", MID_WIDTH_LETTER - 2, HEIGHT_LETTER * (1/2) - (6.5 * inch * .4) / 2, width = 20, height = 6.5 * inch * .4)
    c.drawImage(prefix+dir_signature+de_novo+"_legend.png", MID_WIDTH_LETTER, HEIGHT_LETTER - 1 * inch - 5, width =1.5 * inch, height=legend_dims[num_extracted])
    c.drawImage("lib/Accolade_fermante.png", MID_WIDTH_LETTER - 15, HEIGHT_LETTER * (1/8), width = 15, height = HEIGHT_LETTER * (3/4))


    # THIS IS THE RIGHT SIDE, IT CHANGES
    num_bases = len(bases)
    # print("num bases is: " + str(num_bases))
    if (num_bases == 1):
        plot_1(de_novo, bases, prefix, c)
    elif (num_bases == 2):
        plot_2(de_novo, bases, prefix, c)
    elif (num_bases == 3):
        plot_3(de_novo, bases, prefix, c)
    elif (num_bases == 4):
        plot_4(de_novo, bases, prefix, c)
    elif (num_bases == 5):
        plot_5(de_novo, bases, prefix, c)
    else:
        print("ERROR: Attempted to plot graph with more than five basis signatures.")
    c.showPage()


# iterate over the csv file and generate plots accordingly
def gen_decomposition(sample_dir, output_dir):
    # Note: 0th index contains the title of the column
    de_novo = []
    global_nmf = []
    l1_err = []
    l2_err = []
    cos_similarity = []

    csv_path = sample_dir + "/" + output_dir + "/DBS78/Suggested_Solution/Decomposed_Solution/" + comparison_file_name
    prefix = sample_dir + "/"
    c = canvas.Canvas(sample_dir + "/" + output_dir + "/DBS78/Suggested_Solution/Decomposed_Solution/SignatureDecompositions_DBS78" + ".pdf", pagesize=letter)
    c.setPageSize(landscape(letter))
    c.setFont("Arial", 9)

    with open(csv_path) as csv_file:
        data = csv.reader(csv_file, delimiter= ",")
        for row in data:
            de_novo.append(row[0])
            global_nmf.append(row[1])
            cos_similarity.append(row[4])

    for i in range(1, len(de_novo)):
        c.setFont("Arial", 9)
        g_nmf_split = global_nmf[i].split("&")
        basis_plots = [] # list of pairs (x,y) where x = basis signature, y = contribution percentage
        basis_contribution = []

        for j in range(0, len(g_nmf_split)):
            basis_plots.append([glob_nmf_parse(g_nmf_split[j])[PLOT_NAME],glob_nmf_parse(g_nmf_split[j])[CONTRIBUTION]])

        tmp_sig = de_novo_parse(de_novo[i])
        # generate the stacked percentile bar and legend
        pie_figs.gen_figures(basis_plots, sample_dir+"/cosmic_and_denovo_pngs/SPExtractor_DBS78_Signature_png/" + tmp_sig)
        gen_plot(tmp_sig, basis_plots, cos_similarity[i], prefix, c)


    shutil.rmtree(sample_dir + "/cosmic_and_denovo_pngs/")
    c.save()

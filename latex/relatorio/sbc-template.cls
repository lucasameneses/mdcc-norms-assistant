%%
%% SBC Brazilian Symposia Template - sbc-template.cls
%% Based on the official SBC template format
%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{sbc-template}[2024/01/01 SBC Template]

\LoadClass[12pt,a4paper]{article}

\RequirePackage{times}
\RequirePackage{graphicx}
\RequirePackage{url}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}

%% Page layout
\RequirePackage[a4paper,
                top=3.5cm,
                bottom=2.5cm,
                left=3.0cm,
                right=3.0cm]{geometry}

\pagestyle{empty}
\setlength{\parindent}{1.27cm}
\setlength{\parskip}{6pt}

%% Section formatting
\RequirePackage{titlesec}
\titleformat{\section}{\normalfont\bfseries\normalsize}{\thesection.}{0.5em}{}
\titleformat{\subsection}{\normalfont\bfseries\normalsize}{\thesubsection.}{0.5em}{}
\titleformat{\subsubsection}{\normalfont\bfseries\normalsize}{\thesubsubsection.}{0.5em}{}

\titlespacing{\section}{0pt}{12pt}{6pt}
\titlespacing{\subsection}{0pt}{12pt}{6pt}
\titlespacing{\subsubsection}{0pt}{12pt}{6pt}

%% Captions
\RequirePackage{caption}
\captionsetup{font=small, labelfont=bf, justification=centering}

%% Author/affiliation support (SBC style)
\newcommand{\inst}[1]{\textsuperscript{#1}}
\newcommand{\address}[1]{\def\@address{#1}}
\newcommand{\email}[1]{\texttt{#1}}
\def\@address{}

%% Title block
\def\@maketitle{%
  \begin{center}
    {\Large\bfseries \@title \par}%
    \vskip 0.5em%
    {\normalsize \@author \par}%
    \vskip 0.3em%
    {\small \@address \par}%
  \end{center}%
  \vskip 1em
}

%% Abstract environment
\renewenvironment{abstract}{%
  \vspace{0.5em}
  \begin{center}
    \begin{minipage}{0.95\textwidth}
    \textbf{Abstract.} \itshape
}{%
    \end{minipage}
  \end{center}
  \vspace{0.5em}
}

%% Resumo environment
\newenvironment{resumo}{%
  \vspace{0.5em}
  \begin{center}
    \begin{minipage}{0.95\textwidth}
    \textbf{Resumo.} \itshape
}{%
    \end{minipage}
  \end{center}
  \vspace{1em}
}

\newcommand{\palavraschave}[1]{%
  \vspace{0.5em}
  \noindent\textbf{Palavras-chave:} #1
}

\newcommand{\keywords}[1]{%
  \vspace{0.5em}
  \noindent\textbf{Keywords:} #1
}

\setlength{\baselineskip}{18pt}

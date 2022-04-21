%{
Author:
Date:
Abstract:
%}

% Clear console and workspace
clear, clc;
% Format (short: 5; long: 16; e: always exponential; eng: engineering format (10.56e(+-22)); g: automatic)
format long g;

% Non-zero if running on Octave
isOctave = exist('OCTAVE_VERSION', 'builtin');

% Checks for existence
if ( (exist("someVar","var")~=1) || (exist("someVar2","var")~=1) ) % These vars must exist
    error("Required vars are not initialized");
end
if exist("script", "file") ~= 2 % This script must be in the working directory
    error("Cannot find required script in directory");
end

% Checks for existence of folder. If not found, then it is created
folder = "Example_folder"
if (exist(folder, "dir")~=7)
    disp("Message. '"+folder+"' isn't in current folder. Creating folder...");
    [status, msg] = mkdir(export_folder);
    if status==0 % This means folder couldn't be created
        error(msg);
    end
    disp(msg);
end

disp("End of program");

# phys350-code
Python code for PHYS 350 Project

Objectives will be added in this README file. When writing processes, add additional python script files rather than modifying the main file.

The general process to follow for the icicle growth analysis are as follows:

- Load image of icicle using OpenCV, and calculate left and right bounds using thresholding and OpenCV Canny.
- Calculate the spine of the icicle using the midpoints of the lest and right bounds.
- If the spine is sufficiently curved (threshold TBD), perform a linear fit to renormalize the spine with.
- Using the (possible renormalized) spine of the icicle, re-adjust the left and right bounds so the position of the spine is zero.
- Fit the adjusted left and right bounds to the icicle response function.
- Investigate differences in fit parameters between left and right halves (investigation process TBD)
Re-iterate this process over icicle growth, comparing every 4 frames (since these frames will have the same side of the icicle facing the camera).

Color analysis for icicles grown with colored contaminants not yet decided.

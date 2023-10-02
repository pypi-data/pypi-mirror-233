# Monte-Carlo-Neural-Nets

A package meant to demonstrate how well deep neural nets could be with random weight assignment / training (hence monte-carlo). Similar to popular machine learning packages in python, the created nets can consist of many layers, all custom in size, with different activation functions in between each layer to achieve the desire results (note the curve fitting example on the github page below).

By either having some data set to fit a model to, or by having some 'score' factor, the nets can be trained in a large variety of situations. For example, curve fitting, playing Snake, playing Chess, etc., have all successfully been done so far.

<!-- A package made to see how well a basic architecture of neural nets could be. The nets can be created with custom input and output heights, as well as full customization of the hidden layers' sizes (height and count of layers).

The basic operation of these nets is that they can be trained to some data set (or not, currently working on a 'self-training' chess AI example) by randomly 'tweaking' the different parameter weight values within the net. These weight values are clipped to be restrained to the range [-1, 1].

By defualt, a ELU-type function is applied at every layer calculation to give non-linearites such that more advanced calculations are actually possible. -->

Some examples of the net's operation and training can be found on the GitHub page, where issues are also tracked:
https://github.com/SciCapt/Monte-Carlo-Neural-Nets
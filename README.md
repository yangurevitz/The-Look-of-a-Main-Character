# The Look of a Main Character

This project is about analysing the correlations between visual and narrative features, with the medium of anime as an example.
The project uses the results of Neural Network based classification and a human survey to compare the patterns found in both methods.

The goal of the project is to better understand how humans and neural 
networks compare in the task of classifying characters based purely on
their character design, which patterns emerge from each group
and how it relates to expectations associated with different 
visual features. The knowledge from such an analysis can be used
in the entertainment industry to help create character designs that follow
(or purposefully subvert) audience expectations.

Parts of this project, especially the classification neural network, could
also possibly be used in automatic character generation, to combine
narrative adn visual features in the generation parameters.

In this repository you'll find code responsible for collecting labelled character images from the internet, 
training a ResNet50 model on the calssificaiton task, running the human survey on Google Colab, and analysing and visualising the results.
On top of that, you'll also find the original data used for the project.

Every Notebook contains documentation about its purpose and about how to use and make changes to it.

## Running the code

You can choose to just analyse the results of our experiments, 
or to run your own, in which case you can either use our data or collect your own.
You can find our trained weights [here](https://drive.google.com/file/d/1o737-P8PvCkMq6gF5nq2gGtoImzoWvZi/view?usp=sharing).

### Analysing our results

If your aim is simply to further analyse the results of our experiments,
you can just run “Results Analysis.ipynb” and follow its structure to
explore the questions and patterns you have in mind.

### Running your experiments with the original data

For this, you’ll probably want to train your own model, possibly using 
“ResNet/Train and Eval.ipynb” as an example. 

You might also want to 
run your own survey. For that, simply upload “Human Classification Test/Human Classification Test.ipynb”
to your drive to use it on colab. Note that you’ll also want to upload
the images to your drive. After that, you can use
“Human Classification Test/Generate JSON.ipynb” to format the results
of the survey as expected by “Results Analysis.ipynb”. When that is done, you can run the analysis Notebook.

### Running your experiments with new data

After collecting the images you can filter them however you want, and extract your desired visual features. 
In our case we used [Rasta](https://github.com/bnegreve/rasta) and [CLIP](https://github.com/openai/CLIP) 
to limit ourselves to only human characters who fit the dominant artistic styles. 
We extracted our desired visual features with [CLIP](https://github.com/openai/CLIP) and 
[Illustration2Vec](https://github.com/rezoo/illustration2vec). 
You can find more about how to use them on their respective Github pages linked above.

After getting your desired dataset and extracting the visual features from 
it, you can just follow the instructions in the previous section.

## Common characters structure

This section exists to clarify the structure used to store character
Information throughout the code, usually given the variable name “characters”.

The structure is a dictionary as follows

characters  = 
{
	“Main”: 
{
	mainCharacter0: info, 
	mainCharacter1: info, 
	.
	.
	.
	mainCharacterN-1: info
}
“Supporting”: 
{
	supportingCharacter0: info, 
	supportingCharacter1: info, 
	.
	.
	.
	supportingCharacterN-1: info
}
}

Note that “Main” and “Supporting” can be replaced by your desired
classes and that each character is identified by their name.

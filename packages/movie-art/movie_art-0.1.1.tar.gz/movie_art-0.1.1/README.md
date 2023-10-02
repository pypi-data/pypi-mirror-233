# Movie Art
Turn your favorite movies into their 1D representation, where each pixel column 
corresponds to the average color of a given frame in the movie.


## Examples
Barbie (2023)

![Barbie (2023)](img/barbie_output.jpg)

Pulp Fiction (1994)

![Pulp Fiction (1994)](img/pulp_fiction_output.jpg)

Test Video ([512 frames transitioning from black to white](https://youtu.be/rVVbhl_SVIw))

![Test Video (512 frames transitioning from black to white)](img/test_output.jpg)


## Installation
```sh
pip install movie_art
```


## Usage
```sh
python -m movie_art [input.mp4] [output.jpg] --width [width] --height [height]
```
*i.e.*
```sh
python -m movie_art pulp_fiction.mp4 pulp_fiction_output.jpg --width 512 --height 128
```

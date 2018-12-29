# pixela2img
Create image files (or objects) from Pixela graphs.

#### example

* From this graph(<https://pixe.la/v1/users/pixela2img/graphs/pixela2img?date=20181229>)

![](https://pixe.la/v1/users/pixela2img/graphs/pixela2img?date=20181229)

* Create a `png` image below!

    ![](https://github.com/ryosms/pixela2img/blob/master/docs/pixela2img-pixela2img-20181229.png?raw=true)

## Support

* Python 3.6+

## Usage

Install using `pip`.

```bash
$ pip install pixela2img
```

Create a `png` image with cli.

```bash
$ python -m pixela2img -u pixela2img -g pixela2img -d 20181229
$ open pixela2img-pixela2img-20181229.png
```

or Launch python interpreter and run command below

```hello_pixela.py
from pixela2img import Pixela2Img
pixela = Pixela2Img()

images = []
images.append(pixela.convert(user='pixela2img', graph='pixela2img', date='20181201'))
images.append(pixela.convert(user='pixela2img', graph='pixela2img', date='20181208'))
images.append(pixela.convert(user='pixela2img', graph='pixela2img', date='20181215'))
images.append(pixela.convert(user='pixela2img', graph='pixela2img', date='20181222'))
images.append(pixela.convert(user='pixela2img', graph='pixela2img', date='20181229'))

images[0].save('pixela.gif', save_all=True, append_images=images[1:], loop=0)
```

Created animation gif below!

![](https://github.com/ryosms/pixela2img/blob/master/docs/pixela.gif?raw=true)

## for Developer

#### require

* Python 3.7+
* pipenv

#### prepare

1. clone (or fork) this repository.
2. install dependencies with pipenv
3. edit code!

```bash
$ git clone https://github.com/ryosms/pixela2img
$ cd pixela2img
$ pipenv install
```

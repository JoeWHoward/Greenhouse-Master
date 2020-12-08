![Wagtail](https://miro.medium.com/max/2536/1*qkPzyorkZ1-1NXbMLiE6gg.jpeg)

# wag-commerce project - Skypiea Store
E-Commerce Site using Django, Wagtail and Snipcart

## Table of contents

- [Setting up the project](#setting-up-the-project)
- [Setting up the project with Docker](#setting-up-the-project-with-docker)
- [Cleaning up the Container and Image](#cleaning-up-the-container-and-image)
- [Inspiration](#inspiration)
- [Contact](#contact)

## Setting up the project

  Start by cloning the project with the command:
  ```
  $ git clone https://github.com/rmiyazaki6499/wag-commerce.git
  ```
  
  ## Setting up the project with Docker

  For those that are not interested in setting up the project manually or would simply not have to worry about downloading node.js and its dependencies, I have      created a Dockerfile and docker-compose.yml file to help create a container with everything you would need to run the **wag-commerce**.

  ### Install Docker

  To make this as easy as possible, we will be using *Docker Compose* to creat our container.

  - If you do not have Docker yet, start by downloading it if you are on a Mac or Windows:
  https://www.docker.com/products/docker-desktop

  - Or if you are on a Linux Distribution follow the directions here:
  https://docs.docker.com/compose/install/

  - To confirm you have Docker Compose, open up your terminal and run the command below:

  ```
  $ docker-compose --version
  docker-compose version 1.26.2, build eefe0d31
  ```
  
  - Go into the project directory to build and run the container with:

  ```
  $ cd wag-commerce/
  $ docker-compose up -d --build
  ```

  **This may take a few moments**
  
  Navigate to http://localhost:8000 to view the site on the local server.
It should look something like this:

**Home Page**
![Skypiea Store Home](https://user-images.githubusercontent.com/41876764/90873445-08f0a200-e353-11ea-995e-35291338f318.png)

**Product Page**
![Breath Dial Details](https://user-images.githubusercontent.com/41876764/90873592-3e958b00-e353-11ea-8184-d0f61f23d91c.png)

**Checkout**
![Snipcart](https://user-images.githubusercontent.com/41876764/90873643-54a34b80-e353-11ea-8fc8-0b28f7166cf2.png)
  
  ### Cleaning up the Container and Image

  - To stop the container from running, use `<Ctrl-C>` twice.
  - To close down the container use the command:

  ```
  $ docker-compose down
  ```
  - Then to clean up the container and image which we are no longer using use the command:

  ```
  $ docker system prune -fa
  ```

  - Confirm that the container and image is no longer there with:

  ```
  $ docker system df -v
  ```

## Inspiration

[E-Commerce for Django Developers with Wagtail Tutorial
by Charles Ouellet]
(https://snipcart.com/blog/django-ecommerce-tutorial-wagtail-cms)

## Contact

[Ryuichi Miyazaki](https://github.com/rmiyazaki6499)

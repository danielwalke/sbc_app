# Use the official Node.js image as a base image
FROM node:14 as builder

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application code
COPY .. .

# Build the application
RUN npm run build

# Use a smaller base image for the production build
FROM node:14-alpine

# Set the working directory
WORKDIR /app

# Copy only the built artifacts from the previous stage
COPY /dist /app/dist

# Expose the port that your application will run on
EXPOSE 3000

# Install serve to run the application
RUN npm install -g serve

# Command to run the application
CMD ["serve", "-s", "dist"]

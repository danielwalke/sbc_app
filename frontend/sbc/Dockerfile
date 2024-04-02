# Use the official Node.js image as a base image
FROM node:16.14.0-alpine

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

# Copy only the built artifacts from the previous stage
COPY /dist /app/dist

# Expose the port that your application will run on
EXPOSE 4173

# Install serve to run the application
#RUN npm install -g serve
RUN npm install

# Command to run the application
#CMD ["serve", "-s", "dist"]
CMD ["npm", "run", "preview"]

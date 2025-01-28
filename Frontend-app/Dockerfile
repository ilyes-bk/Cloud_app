FROM node:20

WORKDIR /app

# Copy package.json and package-lock.json
COPY ./Frontend-app /app

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 3000

CMD ["npm", "run", "dev"]
FROM node:20-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# Build the application
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
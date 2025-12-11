FROM node:20-alpine

WORKDIR /app

RUN apk add --no-cache make

COPY package*.json ./

RUN npm ci

COPY . .

CMD ["npm", "run", "build"]

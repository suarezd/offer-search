FROM node:20-alpine

WORKDIR /app

RUN apk add --no-cache make

COPY package*.json ./

RUN npm ci

COPY . .

RUN chown -R node:node /app

USER node

CMD ["npm", "run", "build"]

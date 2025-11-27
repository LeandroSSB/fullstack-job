FROM node:18.17.0-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci --legacy-peer-deps

COPY . .

RUN npm run build

RUN npm prune --production --legacy-peer-deps

EXPOSE 3000

ENV HOSTNAME=0.0.0.0

CMD ["npm", "start"]
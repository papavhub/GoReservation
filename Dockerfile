FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY . .

# swag CLI (라이브러리와 호환되는 버전으로 고정)
RUN go install github.com/swaggo/swag/cmd/swag@v1.16.2

# Swagger 문서 생성
RUN swag init

# 의존성 정리
RUN go mod tidy

# 빌드
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o app

FROM alpine:latest

WORKDIR /app
COPY --from=builder /app/app .
COPY --from=builder /app/docs ./docs

EXPOSE 8080
CMD ["./app"]

FROM golang:1.22-alpine AS builder

WORKDIR /app

# 소스 전체 복사
COPY . .

# 의존성 정리 (go.sum 생성)
RUN go mod tidy

# 빌드
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o app

FROM alpine:latest

WORKDIR /app
COPY --from=builder /app/app .

EXPOSE 8080
CMD ["./app"]

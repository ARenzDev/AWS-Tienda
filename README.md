# Proyecto: Infraestructura como Código en AWS

## Descripción

Sistema basado en **AWS CDK** para gestionar eventos con **EventBridge**, autenticación mediante **Amazon Cognito**, y funciones **AWS Lambda** conectadas a una base de datos **DynamoDB**. Incluye un módulo frontend para administrar usuarios desarrollado con **React + Vite**.

---

## Arquitectura

- **Backend**:
  - **Amazon Cognito**: Autenticación y autorización.
  - **AWS EventBridge**: Enrutamiento de eventos hacia funciones Lambda.
  - **AWS Lambda**:
    - Gestión de pedidos en las tiendas "Don Pedro" y "Panadería Familiar".
    - CRUD de usuarios.
  - **DynamoDB**: Almacenamiento de pedidos y usuarios.
- **Frontend**:
  - **React + Vite**: Desarrollo del CRUD de usuarios.

---

## Stack Tecnológico

- **Infraestructura como Código**: AWS CDK.
- **Servicios de AWS**:
  - Cognito
  - EventBridge
  - Lambda
  - DynamoDB
  - CloudWatch (monitoreo y logs).
- **Frontend**:
  - React + Vite
  - Axios (para consumo de APIs).

---

## Configuración y Despliegue

### Backend

1. Instalar dependencias:

   ```bash
   npm install
   ```

2. Configurar AWS CDK

    ```bash
    cdk bootstrap
    ```

3. Desplegar infraestructura

    ```bash
    cdk deploy
    ```

### Frontend

1. Crear proyecto con vite

    ```bash
    npm create vite@latest
    ```

2. Instalar dependencias

    ```bash
    cd app
    npm install
    ```

3. Ejecutar proyecto

    ```bash
    npm run dev
    ```

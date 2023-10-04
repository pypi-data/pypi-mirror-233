# go-project-cli

Golang Project Folder and File Creation CLI

---

# Command

## new

- create package with Controller, Service, Model, Repository
- projectcli new [package name]

   ```bash
  projectcli new [package name]
   ```
- Examples of executions
  ```text
    .
    └── package_name/
      ├── controllers/
      │   └── controller.go
      ├── services/
      │   └── service.go
      ├── repositories/
      │   └── repository.go
      └── models/
          └── model.go
  ```

# generate

- create semantic folders and files such as controllers, services, and models
- projectcli generate [schematic] [package name]
- Examples of executions
    - projectcli generate co [package name]
      ```text
        .
        └── controllers/
          └── controller.go
      ```

### semantics

|    name    | alias |            description             |
|:----------:|:-----:|:----------------------------------:|
| controller |  co   | Generate a controller declaration. |
|  service   |   s   |  Generate a service declaration.   |
|   model    |   m   |   Generate a model declaration.    |
| repository |   r   | Generate a repository declaration. |
# Establish provider

provider "aws" {
  region = "eu-west-2"
}

# Refer to existing resources

data "aws_vpc" "c9-vpc" {
  id = "vpc-04423dbb18410aece"
}

data "aws_ecs_cluster" "c9-cluster" {
  cluster_name = "c9-ecs-cluster"
}

data "aws_ecr_repository" "c9-zander-trucks-pipeline-repo" {
  name = "c9-zander-trucks"
}

data "aws_ecr_repository" "c9-zander-trucks-dashboard-repo" {
  name = "c9-zander-trucks-dashboard"
}

data "aws_ecr_repository" "c9-zander-trucks-report-repo" {
  name = "c9-zander-trucks-report"
}

data "aws_iam_role" "execution-role" {
  name = "ecsTaskExecutionRole"
}

# Task Definition

resource "aws_ecs_task_definition" "dash-task-def" {
  family = "c9-zander-trucks-dashboard-terraform"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn = data.aws_iam_role.execution-role.arn
  container_definitions = jsonencode([
    {
      "name": "c9-zander-trucks-dashboard-terraform",
      "image": "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c9-zander-trucks-dashboard:latest",
      "essential": true,
      "portMappings": [
          {
            "containerPort": 1243,
            "hostPort": 1243,
            "appProtocol": "http",
            "protocol": "tcp"
          }
        ],
        "environment": [
        {
            "name": "DB_USERNAME",
            "value": var.DB_USERNAME
        },
        {
            "name": "DB_HOST",
            "value": var.DB_HOST
        },
        {
            "name": "DB_NAME",
            "value": var.DB_NAME
        },
        {
            "name": "DB_PASSWORD",
            "value": var.DB_PASSWORD
        },
        {
            "name": "DB_PORT",
            "value": var.DB_PORT
        }
        ]
    }
  ])
}

resource "aws_ecs_service" "dash-service" {
  name = "c9-zander-dash-service-tf"
  cluster = data.aws_ecs_cluster.c9-cluster.id
  task_definition = aws_ecs_task_definition.dash-task-def.arn
  desired_count = 1
  launch_type = "FARGATE"
  network_configuration {
    subnets = ["subnet-0d0b16e76e68cf51b", "subnet-081c7c419697dec52", "subnet-02a00c7be52b00368"]
    security_groups = ["sg-07ca57f113e52999d"]
    assign_public_ip = true
  }

}
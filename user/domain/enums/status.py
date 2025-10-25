from enum import Enum


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"
    
    def __repr__(self):
        return self.value


class SagaStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"
    
    def __repr__(self):
        return self.value


class StepStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATED = "compensated"
    
    def __repr__(self):
        return self.value


class MessageType(str, Enum):
    COMMAND = "command"
    RESPONSE = "response"
    COMPENSATION = "compensation"
    
    def __repr__(self):
        return self.value
    

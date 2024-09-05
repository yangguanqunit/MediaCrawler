import enum

class NoteType(enum.Enum):
    LongDurationNote = 1  # 超长期特别国债
    DiscountNote = 2      # 贴现式国债
    InterestNote = 3      # 付息式国债
    Other = 4             # 其他类型国债
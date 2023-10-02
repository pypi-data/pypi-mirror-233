class TimerInitError(ValueError):
    pass


class Timer:
    def __init__(self, default=30, min_=None, max_=None, change_rate=None):
        self.default = default
        self.min_ = min_
        self.max_ = max_
        self.change_rate = change_rate
        self.next = self.default
        self.check_init()

    def check_init(self):
        if self.min_ is not None and self.max_ is not None:
            if self.min_ > self.max_:
                raise TimerInitError(f"min_ must be smaller than max_, got {self.min_} and {self.max_}")
        if self.change_rate is not None:
            if self.change_rate <= 1:
                raise TimerInitError(f"change_rate must be greater than 1, got {self.change_rate}")
        if self.min_ is None and self.max_ is None and self.change_rate is None:
            raise TimerInitError("At least one of min_, max_, or change_rate must be set")

    def __call__(self, status: bool = None):
        if status is None:
            return self.next
        if status:
            if self.max_ is not None:
                self.next = (self.next + self.max_) >> 1
            else:
                self.next = self.next * self.change_rate
        else:
            if self.min_ is not None:
                self.next = (self.next + self.min_) >> 1
            else:
                self.next = self.next // self.change_rate
        return self.next

    def reset(self):
        self.next = self.default

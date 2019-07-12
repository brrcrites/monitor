
class GCPStatus:
    def __init__(self, service_name, begin, end, severity_level):
        self.service = service_name
        self.start_time = begin
        self.end_time = end
        self.severity = severity_level

    def __str__(self):
        return ('[%s - %s] [%s] %s' % (self.start_time, self.end_time, self.severity, self.service))

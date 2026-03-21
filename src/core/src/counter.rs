use crate::LogLevel;

pub struct SeverityCounter {
    verbose: usize,
    debug: usize,
    info: usize,
    warning: usize,
    error: usize,
    fatal: usize,
}

impl SeverityCounter {
    pub fn new() -> Self {
        Self {
            verbose: 0,
            debug: 0,
            info: 0,
            warning: 0,
            error: 0,
            fatal: 0,
        }
    }

    pub fn add(&mut self, level: LogLevel) {
        match level {
            LogLevel::Verbose => self.verbose += 1,
            LogLevel::Debug => self.debug += 1,
            LogLevel::Info => self.info += 1,
            LogLevel::Warning => self.warning += 1,
            LogLevel::Error => self.error += 1,
            LogLevel::Fatal => self.fatal += 1,
            LogLevel::Unknown => {}
        }
    }

    pub fn total(&self) -> usize {
        self.verbose + self.debug + self.info + self.warning + self.error + self.fatal
    }
}

impl Default for SeverityCounter {
    fn default() -> Self {
        Self::new()
    }
}

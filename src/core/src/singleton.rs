use std::sync::OnceLock;

static INSTANCE: OnceLock<String> = OnceLock::new();

pub fn get_singleton() -> &'static String {
    INSTANCE.get_or_init(|| "singleton instance".to_string())
}

pub fn reset_singleton() {
    let _ = INSTANCE.set(String::new());
}

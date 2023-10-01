use std::error::Error;

#[cfg(target_os = "windows")]
mod winapi;

mod chromium;
mod paths;
mod sqlite;
mod mozilla;
mod utils;
mod enums;
mod config;
pub use chromium::chromium_based;
pub use mozilla::firefox_based;
pub use enums::*;


/// Returns cookies from all browsers
///
/// # Arguments
///
/// * `domains` - A optional list that for getting specific domains only
///
/// # Examples
///
/// ```
/// use rookie;
/// 
/// fn main() {
///     let domains = vec!["google.com"];
///     let cookies = rookie::load(Some(domains));
/// }
/// ```
pub fn load(domains: Option<Vec<&str>>) -> Result<Vec<Cookie>, Box<dyn Error>> {
    let mut cookies = Vec::new();

    let firefox_cookies = firefox(domains.clone()).unwrap_or(vec![]);
    cookies.extend(firefox_cookies);


    let chrome_cookies = chrome(domains.clone()).unwrap_or(vec![]);
    cookies.extend(chrome_cookies);


    let brave_cookies = brave(domains.clone()).unwrap_or(vec![]);
    cookies.extend(brave_cookies);

    let edge_cookies = edge(domains).unwrap_or(vec![]);
    cookies.extend(edge_cookies);

    Ok(cookies)
}

/// Returns cookies from firefox
///
/// # Arguments
///
/// * `domains` - A optional list that for getting specific domains only
///
/// # Examples
///
/// ```
/// use rookie;
/// 
/// fn main() {
///     let domains = vec!["google.com"];
///     let cookies = rookie::firefox(Some(domains));
/// }
/// ```
pub fn firefox(domains: Option<Vec<&str>>) -> Result<Vec<Cookie>, Box<dyn Error>> {
    let db_path = paths::find_mozilla_based_paths(&config::FIREFOX_CONFIG)?;
    firefox_based(db_path, domains)
}

/// Returns cookies from libre wolf
///
/// # Arguments
///
/// * `domains` - A optional list that for getting specific domains only
///
/// # Examples
///
/// ```
/// use rookie;
/// 
/// fn main() {
///     let domains = vec!["google.com"];
///     let cookies = rookie::libre_wolf(Some(domains));
/// }
/// ```
pub fn libre_wolf(domains: Option<Vec<&str>>) -> Result<Vec<Cookie>, Box<dyn Error>> {
    let db_path = paths::find_mozilla_based_paths(&config::LIBRE_WOLF_CONFIG)?;
    firefox_based(db_path, domains)
}


/// Returns cookies from chrome
///
/// # Arguments
///
/// * `domains` - A optional list that for getting specific domains only
///
/// # Examples
///
/// ```
/// use rookie;
/// 
/// fn main() {
///     let domains = vec!["google.com"];
///     let cookies = rookie::chrome(Some(domains));
/// }
/// ```
pub fn chrome(domains: Option<Vec<&str>>) -> Result<Vec<Cookie>, Box<dyn Error>> {
    let (key, db_path) = paths::find_chrome_based_paths(&config::CHROME_CONFIG)?;
    chromium_based(key, db_path, domains)
}

/// Returns cookies from chromium
///
/// # Arguments
///
/// * `domains` - A optional list that for getting specific domains only
///
/// # Examples
///
/// ```
/// use rookie;
/// 
/// fn main() {
///     let domains = vec!["google.com"];
///     let cookies = rookie::chromium(Some(domains));
/// }
/// ```
pub fn chromium(domains: Option<Vec<&str>>) -> Result<Vec<Cookie>, Box<dyn Error>> {
    let (key, db_path) = paths::find_chrome_based_paths(&config::CHROMIUM_CONFIG)?;
    chromium_based(key, db_path, domains)
}


/// Returns cookies from brave
///
/// # Arguments
///
/// * `domains` - A optional list that for getting specific domains only
///
/// # Examples
///
/// ```
/// use rookie;
/// 
/// fn main() {
///     let domains = vec!["google.com"];
///     let cookies = rookie::brave(Some(domains));
/// }
/// ```
pub fn brave(domains: Option<Vec<&str>>) -> Result<Vec<Cookie>, Box<dyn Error>> {
    let (key, db_path) = paths::find_chrome_based_paths(&config::BRAVE_CONFIG)?;
    chromium_based(key, db_path, domains)
}


/// Returns cookies from edge
///
/// # Arguments
///
/// * `domains` - A optional list that for getting specific domains only
///
/// # Examples
///
/// ```
/// use rookie;
/// 
/// fn main() {
///     let domains = vec!["google.com"];
///     let cookies = rookie::edge(Some(domains));
/// }
/// ```
pub fn edge(domains: Option<Vec<&str>>) -> Result<Vec<Cookie>, Box<dyn Error>> {
    let (key, db_path) = paths::find_chrome_based_paths(&config::EDGE_CONFIG)?;
    chromium_based(key, db_path, domains)
}

/// Returns cookies from vivaldi
///
/// # Arguments
///
/// * `domains` - A optional list that for getting specific domains only
///
/// # Examples
///
/// ```
/// use rookie;
/// 
/// fn main() {
///     let domains = vec!["google.com"];
///     let cookies = rookie::vivaldi(Some(domains));
/// }
/// ```
pub fn vivaldi(domains: Option<Vec<&str>>) -> Result<Vec<Cookie>, Box<dyn Error>> {
    let (key, db_path) = paths::find_chrome_based_paths(&config::VIVALDI_CONFIG)?;
    chromium_based(key, db_path, domains)
}


/// Returns cookies from opera
///
/// # Arguments
///
/// * `domains` - A optional list that for getting specific domains only
///
/// # Examples
///
/// ```
/// use rookie;
/// 
/// fn main() {
///     let domains = vec!["google.com"];
///     let cookies = rookie::opera(Some(domains));
/// }
/// ```
pub fn opera(domains: Option<Vec<&str>>) -> Result<Vec<Cookie>, Box<dyn Error>> {
    let (key, db_path) = paths::find_chrome_based_paths(&config::OPERA_CONFIG)?;
    chromium_based(key, db_path, domains)
}

/// Returns cookies from opera gx
///
/// # Arguments
///
/// * `domains` - A optional list that for getting specific domains only
///
/// # Examples
///
/// ```
/// use rookie;
/// 
/// fn main() {
///     let domains = vec!["google.com"];
///     let cookies = rookie::opera_gx(Some(domains));
/// }
/// ```
pub fn opera_gx(domains: Option<Vec<&str>>) -> Result<Vec<Cookie>, Box<dyn Error>> {
    let (key, db_path) = paths::find_chrome_based_paths(&config::OPERA_GX_CONFIG)?;
    chromium_based(key, db_path, domains)
}
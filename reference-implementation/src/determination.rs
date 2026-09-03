use serde_json::{Value, json};

pub fn determine(fixture: &Value, policy: &Value) -> Value {
    let x=&fixture["input"];
    if !x["authority_valid"].as_bool().unwrap_or(false) { return json!({"kind":"NOT_ADMIT","reason_code":"DENIED_AUTHORITY"}); }
    if x["amount"].as_i64().unwrap_or(0) > policy["limits"]["transfer_max"].as_i64().unwrap_or(-1) { return json!({"kind":"NOT_ADMIT","reason_code":"DENIED_POLICY_LIMIT"}); }
    if x["balance"].as_i64().unwrap_or(0) < x["amount"].as_i64().unwrap_or(0) { return json!({"kind":"NOT_ADMIT","reason_code":"DENIED_INSUFFICIENT_FUNDS"}); }
    if x["risk"].as_str() == Some("elevated") { return json!({"kind":"NOT_ADMIT","reason_code":"DENIED_RISK"}); }
    json!({"kind":"ADMIT","reason_code":"APPROVED"})
}

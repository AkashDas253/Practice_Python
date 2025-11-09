// Test file with errors for Mini Lex
int main() {
    int x = 42;
    float y = 3.14;
    x = x + 1;
    $invalid_token
    string s = "Hello;
    char c = 'z';
    /* Unclosed comment
    return x;
}

# **Encryption Package**

This Python package provides basic functionality for encrypting and decrypting strings.

## **Functions**

### `encrypt_str`

The `encrypt_str` function is used to encrypt a string using a specified key.

```python
encrypt_str(Input: str, Key: str = "", Method: int = 0) -> str
```

- `Input`: The string to be encrypted.
- `Key`: The encryption key (optional).
- `Method`: The encryption method (0 for custom encryption).

### `decrypt_str`

The `decrypt_str` function is used to decrypt an encrypted string using a specified key.

```python
decrypt_str(Input: str, Key: str, Method: int = 0) -> str
```

- `Input`: The string to be decrypted.
- `Key`: The decryption key.
- `Method`: The decryption method (0 for custom decryption).

## **Usage**

To use this package, you can call the `encrypt_str` function to encrypt a string and the `decrypt_str` function to decrypt it. Ensure that you provide the correct encryption and decryption keys for successful operations.
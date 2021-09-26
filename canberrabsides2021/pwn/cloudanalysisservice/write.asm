section .text

global _start

_start:
	sub rsp, 1
	push 'A'
	mov rax, 1
	mov rdi, 1
	mov rsi, rsp
	mov rdx, 2
	syscall
	add rsp, 1

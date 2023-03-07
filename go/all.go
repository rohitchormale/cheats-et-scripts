package main

import "fmt"


func main() {
	learnClosures()
	learnRecursion()

}


func learnRecursion() {
	fmt.Println("--- recursion ---")
	fmt.Println(factorial(5))


	fmt.Println("--- recurvsive closure ---")
	fmt.Println("fibonancy series using recursive closure")
	var fib func(n int) int
	fib = func(n int) int {
		if n < 2 {
			return n
		}
		return fib(n-1) + fib(n-2)
	}
	fmt.Println(fib(7))

	fmt.Println("factorial using recursive closure")
	var fact func(n int) int 
	fact = func(n int) int {
		if n == 0 {
			return 1
		}
		return n * fact(n-1) 
	}
	fmt.Println(fact(5))
}


func factorial(n int) int {
	if n == 0 {
		return 1
	}
	return n * factorial(n-1)
}


func learnClosures() {
	fmt.Println("--- closures ---")
	next_number_1 := nextInt()
	fmt.Println(next_number_1()) // output: 1
	fmt.Println(next_number_1()) // output: 2
	fmt.Println(next_number_1()) // output: 3

	next_number_2 := nextInt()
	fmt.Println(next_number_2()) //output: 1

}


func nextInt() func() int {
	i := 0

	return func() int {
		i++
		return i
	}
}


package main

import "fmt"


func nextInt() func() int {
	i := 0

	return func() int {
		i++
		return i
	}
}


func main() {
	learnClosures()

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
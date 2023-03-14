package main

import "fmt"

func main() {
	fmt.Println("\n --- foo loop ---")
	for i := 0; i < 3; i++ {
		j := i + 1
		fmt.Println(i)
		fmt.Println(j)
	} // scope of i,j is in for block only

	// use range to enumerate over string, array, slice, map, channels
	fmt.Println("\n --- for using range --- ")	
	for key, val := range map[int]string{1: "foo", 2: "bar"} {
		fmt.Println(key, val)
	} // range yields 2 vars for string, array, slice, map. For channel it yields only single var

	fmt.Println("\n --- Discard val if not required --- ")	
	for _, val := range "foobar" {
		fmt.Println(val)
	}

	fmt.Println("\n --- infinite loop ---")
	fmt.Println(`for true {
    fmt.Println("I m infinite")
}`)
}

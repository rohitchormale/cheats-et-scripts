package main

import "fmt"


func PrintStr(s []string) {
	fmt.Println("\n --- Printing string slice ---")
	for _, val := range s {
		fmt.Println(val)
	}
}


func PrintInt(i []int) {
	fmt.Println("\n--- Printing int slice ---")
	for _, val := range i {
		fmt.Println(val)
	}
}


func GenericPrint[T any](t []T) {
	fmt.Printf("\n--- Printing %T slice---\n", t)
	for _, val := range t {
		fmt.Println(val)
	}
}

func main() {
	s := []string{"foo", "bar"}
	PrintStr(s)

	i := []int{1,2,3}
	PrintInt(i)

	GenericPrint(s)
	GenericPrint(i)
}
#include <unity.h>
#include "hello.h"

void setUp(void) {
}

void tearDown(void) {
}

void test_hello() {
    TEST_ASSERT_EQUAL(do_hello(), 123);
}

int main(int argc, char** argv) {
    UNITY_BEGIN();
    RUN_TEST(test_hello);
    UNITY_END();

    return 0;
}

int app_main(int argc, char** argv) {
    return main(argc, argv);
}
from dev_api.descriptor import AppBuilder

if __name__ == '__main__':
    builder = AppBuilder()

    builder.add_parameter('L1', True)
    builder.add_parameter('L2', False)
    builder.add_parameter('L3', False)
    builder.add_parameter('L4', False)
    builder.add_parameter('L5', False)
    builder.add_parameter('L6', False)
    builder.add_parameter('L7', False)
    builder.add_parameter('L8', True)

    builder.add_button('L1',['L1'],lambda l1: print(f'It works! Value of L1: {l1}'))
    builder.add_button('L8',['L8'],lambda l8: print(f'It works! Value of L8: {l8}'))
    builder.add_button('L8',['L8'],lambda l8: print(f'It works! Value of L8: {l8}'))
    builder.add_button('L8',['L8'],lambda l8: print(f'It works! Value of L8: {l8}'))
    builder.add_button('L8',['L8'],lambda l8: print(f'It works! Value of L8: {l8}'))
    builder.add_button('L8',['L8'],lambda l8: print(f'It works! Value of L8: {l8}'))
    builder.add_button('L8',['L8'],lambda l8: print(f'It works! Value of L8: {l8}'))

    builder.build_app().run()
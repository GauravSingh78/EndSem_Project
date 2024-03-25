import asyncio
import aiofiles

file_path = 'tree1.txt'
final_data = ""
output_file_path = 'put.txt'


async def search_character_in_lines(data):
    if(data[0]=="*" or data=="\n"):
        pass
    else:
        idx = data.index("|")
        d = data[:idx - 1]
        global final_data
        final_data += d + "\n"
        final_data = final_data.replace("then response:", ": return")
        

async def read_file():
    async with aiofiles.open(file_path, mode='r') as file:
        
        lines = await file.readlines()
        for line in lines:
            print(line)
            await search_character_in_lines(line)
            
async def write_to_file():
    async with aiofiles.open(output_file_path, mode='w') as output_file:
        await output_file.write(final_data)        




async def main():
    await read_file()
    await write_to_file()



if __name__ == "__main__":
    asyncio.run(main())
